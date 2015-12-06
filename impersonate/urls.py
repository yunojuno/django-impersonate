# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import stop_impersonate, list_users, search_users, impersonate


urlpatterns = [
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
]
