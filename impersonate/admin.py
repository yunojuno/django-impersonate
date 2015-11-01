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


class SessionStateFilter(admin.SimpleListFilter):

    """Custom admin filter based on the session state."""

    title = 'session state'
    parameter_name = 'session'

    def lookups(self, request, model_admin):
        return (
            ('incomplete', "Incomplete"),
            ('complete', "Complete")
        )

    def queryset(self, request, queryset):
        print queryset
        if self.value() == 'incomplete':
            return queryset.filter(session_ended_at__isnull=True)
        if self.value() == 'complete':
            return queryset.filter(session_ended_at__isnull=False)
        else:
            return queryset


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
    list_filter = (SessionStateFilter, 'session_started_at')

    def impersonator_(self, obj):
        return friendly_name(obj.impersonator)

    def impersonating_(self, obj):
        return friendly_name(obj.impersonating)

admin.site.register(ImpersonationLog, ImpersonationLogAdmin)
