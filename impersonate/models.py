# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class ImpersonationLog(models.Model):
    ''' Stores details of each impersonation session.

        This model is used to persist details of impersonations. It hooks
        in to the session_begin and session_end signals to capture the
        details of the user impersonating and the user who is being
        impersonated. It also stores the Django session key.

    '''
    impersonator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        help_text=u'The user doing the impersonating.',
        related_name='impersonations',
    )
    impersonating = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='impersonated_by',
        help_text=u'The user being impersonated.',
    )
    session_key = models.CharField(
        max_length=40,
        help_text=u'The Django session request key.',
    )
    session_started_at = models.DateTimeField(
        help_text=u'The time impersonation began.',
        null=True,
        blank=True
    )
    session_ended_at = models.DateTimeField(
        help_text=u'The time impersonation ended.',
        null=True,
        blank=True
    )

    @property
    def duration(self):
        return self._duration()

    def _duration(self):
        from .helpers import duration_string
        if all((self.session_started_at, self.session_ended_at)):
            return duration_string(
                self.session_ended_at - self.session_started_at,
            )
        return u''
    _duration.short_description = u'Duration'
