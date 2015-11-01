# -*- coding: utf-8 -*-
"""Impersonation models."""
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.utils.timezone import now as tz_now

from impersonate.signals import session_begin, session_end

logger = logging.getLogger(__name__)

# if True then ignore the session_begin, session_end logging
DISABLE_SESSION_LOGGING = getattr(settings, 'IMPERSONATE_DISABLE_LOGGING', False)  # noqa


class ImpersonationLog(models.Model):

    """Stores details of each impersonation session.

    This model is used to persist details of impersonations to the local
    database. It hooks in to the session_begin and session_end signals to
    capture the details of the user impersonating and the user who is
    being impersonated. It also stores the Django session key.

    """

    impersonator = models.ForeignKey(
        User,
        help_text="The user doing the impersonating.",
        related_name="impersonations"
    )
    impersonating = models.ForeignKey(
        User,
        related_name="impersonated_by",
        help_text="The user being impersonated."
    )
    session_key = models.CharField(
        max_length="100",
        help_text="The Django session request key."
    )
    session_started_at = models.DateTimeField(
        help_text="The time impersonation began.",
        null=True,
        blank=True
    )
    session_ended_at = models.DateTimeField(
        help_text="The time impersonation ended.",
        null=True,
        blank=True
    )
    # denormalised duration - makes it easier to handle, and should
    # only be written once on session_end.
    duration = models.DurationField(
        help_text="Time spent impersonating.",
        null=True,
        blank=True
    )


@receiver(session_begin)
def on_session_begin(sender, **kwargs):
    """Create a new ImpersonationLog object."""
    impersonator = kwargs.get('impersonator')
    impersonating = kwargs.get('impersonating')
    session_key = kwargs.get('request').session.session_key
    logger.info("%s has started impersonating %s.", impersonator, impersonating)  # noqa

    if DISABLE_SESSION_LOGGING:
        return

    log = ImpersonationLog(
        impersonator=impersonator,
        impersonating=impersonating,
        session_key=session_key,
        session_started_at=tz_now()
    )
    log.save()


@receiver(session_end)
def on_session_end(sender, **kwargs):
    """Update ImpersonationLog with the end timestamp.

    This function relies on the request.session.session_key being the
    same as that used to create the original log.

    """
    impersonator = kwargs.get('impersonator')
    impersonating = kwargs.get('impersonating')
    session_key = kwargs.get('request').session.session_key
    logger.info("%s has finished impersonating %s.", impersonator, impersonating)  # noqa

    if DISABLE_SESSION_LOGGING:
        return

    try:
        # look for unfinished sessions that match impersonator / subject
        log = (
            ImpersonationLog.objects
            .get(
                impersonator=impersonator,
                impersonating=impersonating,
                session_key=session_key,
                session_ended_at__isnull=True
            )
        )
        log.session_ended_at = tz_now()
        log.duration = log.session_ended_at - log.session_started_at
        log.save()
    except ImpersonationLog.DoesNotExist():
        logger.warning(
            "Unfinished ImpersonationLog could not be found for: %s, %s, %s",
            impersonator, impersonating, session_key
        )
    except ImpersonationLog.MultipleObjectsReturned():
        logger.warning(
            "Multiple unfinished ImpersonationLog matching: %s, %s, %s",
            impersonator, impersonating, session_key
        )
