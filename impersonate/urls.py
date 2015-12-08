# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from impersonate.views import impersonate, search_users, list_users, stop_impersonate


urlpatterns = patterns('impersonate.views',
    url(r'^stop/$',
        stop_impersonate,
        name='impersonate-stop'),
    url(r'^list/$',
        list_users,
        {'template': 'impersonate/list_users.html'},
        name='impersonate-list'),
    url(r'^search/$',
        search_users,
        {'template': 'impersonate/search_users.html'},
        name='impersonate-search'),
    url(r'^(?P<uid>.+)/$',
        impersonate,
        name='impersonate-start'),
)
