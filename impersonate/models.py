# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.timezone import now as tz_now


class ImpersonationLog(models.Model):
    ''' Stores details of each impersonation session.

        This model is used to persist details of impersonations. It hooks
        in to the session_begin and session_end signals to capture the
        details of the user impersonating and the user who is being
        impersonated. It also stores the Django session key.

    '''
    impersonator = models.ForeignKey(
        User,
        help_text='The user doing the impersonating.',
        related_name='impersonations',
    )
    impersonating = models.ForeignKey(
        User,
        related_name='impersonated_by',
        help_text='The user being impersonated.',
    )
    session_key = models.CharField(
        max_length=40,
        help_text='The Django session request key.',
    )
    session_started_at = models.DateTimeField(
        help_text='The time impersonation began.',
        null=True,
        blank=True
    )
    session_ended_at = models.DateTimeField(
        help_text='The time impersonation ended.',
        null=True,
        blank=True
    )
    # denormalised duration - makes it easier to handle, and should
    # only be written once on session_end.
    duration = models.DurationField(
        help_text='Time spent impersonating.',
        null=True,
        blank=True
    )
