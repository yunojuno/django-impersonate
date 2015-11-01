#  -*- coding: utf-8 -*-
"""Admin models for impersonate app."""
from django.contrib import admin

from impersonate.models import ImpersonationLog


def friendly_name(user):
    """Return proper name if exists, else username."""
    if user.get_full_name() != '':
        return user.get_full_name()
    else:
        return user.username


class ImpersonationLogAdmin(admin.ModelAdmin):
    list_display = (
        'impersonator_',
        'impersonating_',
        'session_key',
        'session_started_at',
        'duration'
    )
    readonly_fields = (
        'impersonator',
        'impersonating',
        'session_key',
        'session_started_at',
        'session_ended_at',
        'duration'
    )

    def impersonator_(self, obj):
        return friendly_name(obj.impersonator)

    def impersonating_(self, obj):
        return friendly_name(obj.impersonating)

admin.site.register(ImpersonationLog, ImpersonationLogAdmin)
