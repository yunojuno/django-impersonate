# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from impersonate.views import impersonate, search_users, list_users, stop_impersonate


urlpatterns = [
    url(r'^stop/$',
        stop_impersonate,
        name='impersonate-stop',
        prefix='impersonate.views'),
    url(r'^list/$',
        list_users,
        {'template': 'impersonate/list_users.html'},
        name='impersonate-list',
        prefix='impersonate.views'),
    url(r'^search/$',
        search_users,
        {'template': 'impersonate/search_users.html'},
        name='impersonate-search',
        prefix='impersonate.views'),
    url(r'^(?P<uid>.+)/$',
        impersonate,
        name='impersonate-start',
        prefix='impersonate.views'),
]
