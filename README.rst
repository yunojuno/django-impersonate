.. |nlshield| image:: https://img.shields.io/badge/100%25-Netlandish-blue.svg?style=square-flat
              :target: http://www.netlandish.com

==============================
django-impersonate |nlshield|
==============================
:Info: Simple application to allow superusers to "impersonate" other non-superuser accounts.
:Version: 1.3.0
:Author: Peter Sanchez (http://www.petersanchez.com)

Python / Django Support
=======================

* Python 2.7+ for Django versions 1.8 - 1.11
* Python 3.4+ for Django versions 1.9 - 2.0
* Python 3.3 for Django version 1.8

**Note:** In release 1.4 we plan to only support Python 3.4+ and Django 2.0+ moving forward. Bug fixes will be ported to older versions but new feature development will be focusing on modern releases of Python and Django.

Dependencies
============

* Depends on your project using the django.contrib.session framework.

**NOTE:**

* **Version 1.0 adds new functionality by default.** Please see the DISABLE_LOGGING settings option.
* If you need to use this with Django older than 1.8, please use version django-impersonate == 1.0.1
* If you need to use this with Django older than 1.7, please use version django-impersonate == 0.9.2
* **Version 0.9.2 partially reverts work completed in version 0.9.1.** This is because work done to address a request in `Issue #17 <https://bitbucket.org/petersanchez/django-impersonate/issues/17/remember-where-to-return-to-after>`_ broke default behavior for all previous versions. `Issue #24 <https://bitbucket.org/petersanchez/django-impersonate/issues/24/impersonate_redirect_url-no-longer-works>`_ was opened and the fix was released in 0.9.2 to address it. Please see the new USE_HTTP_REFERER settings option.
* If you need to use this with Django older than 1.4, please use version django-impersonate == 0.5.3


Installation
============

PIP::

    pip install django-impersonate

Basic Manual Install::

    $ python setup.py build
    $ sudo python setup.py install

Alternative Install (Manually):

Place impersonate directory in your Python path. Either in your Python installs site-packages directory or set your $PYTHONPATH environment variable to include a directory where the impersonate directory lives.


Use
===

#. Add 'impersonate' to your INSTALLED_APPS

#. Add 'impersonate.middleware.ImpersonateMiddleware' to your MIDDLEWARE_CLASSES

#. Add 'impersonate.urls' somewhere in your url structure. Example::

    urlpatterns = patterns('',
        url(r'^admin/', include(admin.site.urls)),
        url(r'^impersonate/', include('impersonate.urls')),
        ... (all your other urls here) ...
    )

**Note:** The ImpersonationMiddleware class should be placed AFTER the ``django.contrib.auth`` middleware classes

Functionality
=============

**You can now impersonate another user by hitting the following path:**

    /impersonate/<user-id>/

Replace <user-id> with the user id of the user you want to impersonate.

While in impersonation "mode" the request.user object will have an
"is_impersonate" attribute set to True. So if you wanted to check in your
templates or view, you just do something like...::

    {% if user.is_impersonate %} .... {% endif %}

The original user is available as ``request.impersonator``::

    {{ request.user }} ({{ request.impersonator }})

The real user is available as ``request.real_user`` - this is equivalent
to calling ``getattr(request, 'impersonator', request.user)``::

    assert request.real_user == getattr(request, 'impersonator', request.user)

You can reference this URL with reverse() or the {% url %} template tag
as 'impersonate-start' and expects the argument of the user ID. Example::

    reverse('impersonate-start', args=[user.id])
    reverse('impersonate-start', uid=user.id)


**To remove the impersonation, hit the following path:**

    /impersonate/stop/

You can reference this URL with reverse() or the {% url %} template tag
as 'impersonate-stop'. When you call this URL, you will be redirected to
the page that you used to start impersonating a user (eg, some search results
or the user list).


**To list all users you can go to:**

    /impersonate/list/

This will render the template 'impersonate/list_users.html' and will pass
the following in the context:

* users - queryset of all users
* paginator - Django Paginator instance
* page - Current page of objects (from Paginator)
* page_number - Current page number, defaults to 1

You can reference this URL with reverse() or the {% url %} template tag
as 'impersonate-list'.


**To search all users you can go to:**

    /impersonate/search/

This will render the template 'impersonate/search_users.html' and will pass
the following in the context:

* users - queryset of all users
* paginator - Django Paginator instance
* page - Current page of objects (from Paginator)
* page_number - Current page number, defaults to 1
* query - The search query that was entered

The view will expect a GET request and look for the 'q' variable being passed.
If present, it will search the user entries with the value of 'q'. The default
fields searched are:

User.username, User.first_name, User.last_name, User.email

You can reference this URL with reverse() or the {% url %} template tag
as 'impersonate-search'.


**To allow some users to impersonate other users**

You can optionally allow only some non-superuser and non-staff users to impersonate by adding a **CUSTOM_ALLOW** setting option. Create a function that takes a request object, and based on your rules, returns True if the user is allowed to impersonate or not.

**To limit what users a user can impersonate**

By, optionally, setting the **CUSTOM_USER_QUERYSET** option you can control what users can be impersonated. It takes a request object of the user, and returns a QuerySet of users. This is used when searching for users to impersonate, when listing what users to impersonate, and when trying to start impersonation.

Signals
=======

If you wish to hook into the impersonation session (for instance, in order to
audit access), there are two signals that are fired by django-impersonate, at
the beginning and end of a session:

* session_begin - sent when calling the ``impersonate`` view
* session_end - sent when calling the ``stop_impersonate`` view

Both of these signals send the same arguments:

* sender - this is a Django signal requirement, and is always set to None
* impersonator - a reference to the User object of the person doing the impersonation
* impersonating - a reference to the User object of the person being impersonated
* request - the Django HttpRequest object from which the impersonation was invoked

The request object is included as it contains pertinent information that you may wish
to audit - such as client IP address, user-agent string, etc.

For an example of how to hook up the signals, see the relevant test - ``test_successful_impersonation_signals``.

NB The session_end signal will only be fired if the impersonator explicitly ends
the session.

Settings
========

The following settings are available for django-impersonate. All settings should be 
set as variables in a dictionary assigned to the attribute named ``IMPERSONATE``.

For example::

    IMPERSONATE = {
        'REDIRECT_URL': '/some-path/',
        'PAGINATE_COUNT': 10,
    }

**Note:** This is a new format. The old format is now deprecated and support for the old format will be removed in a future release.

Here are the options available...

    REDIRECT_URL

This is the URL you want to be redirected to *after* you have chosen to
impersonate another user. If this is not present it will check for
the LOGIN_REDIRECT_URL setting and fall back to '/' if neither is
present. Value should be a string containing the redirect path.


    USE_HTTP_REFERER

If this is set to True, then the app will attempt to be redirect you to
the URL you were at when the impersonation began once you have *stopped*
the impersonation. For example, if you were at the url '/foo/bar/' when
you began impersonating a user, once you end the impersonation, you will
be redirected back to '/foo/bar/' instead of the value in
REDIRECT_URL.

Value should be a boolean (True/False), defaults to False


    PAGINATE_COUNT

This is the number of users to paginate by when using the list or
search views. This defaults to 20. Value should be an integer.


    REQUIRE_SUPERUSER

If this is set to True, then only users who have 'is_superuser' set
to True will be allowed to impersonate other users. Default is False.
If False, then any 'is_staff' user will be able to impersonate other
users.

**Note:** Regardless of this setting, a 'is_staff' user will **not** be
allowed to impersonate a 'is_superuser' user.

Value should be a boolean (True/False)

If the CUSTOM_ALLOW is set, then that custom function is used, and
this setting is ignored.


    ALLOW_SUPERUSER

By default, superusers cannot be impersonated; this setting allows for that.

**Note:** Even when this is true, only superusers can impersonate other superusers,
regardless of the value of REQUIRE_SUPERUSER.

Value should be a boolean (True/False), and the default is False.


    URI_EXCLUSIONS

Set to a list/tuple of url patterns that, if matched, user
impersonation is not completed. It defaults to::

    (r'^admin/',)

If you do not want to use even the default exclusions then set
the setting to an emply list/tuple.


    CUSTOM_USER_QUERYSET

A string that represents a function (e.g. 'module.submodule.mod.function_name')
that allows more fine grained control over what users a user can impersonate.
It takes one argument, the request object, and should return a QuerySet. Only
the users in this queryset can be impersonated.

This function will not be called when the request has an unauthorised users,
and will only be called when the user is allowed to impersonate (cf.
REQUIRE_SUPERUSER and CUSTOM_ALLOW ).

Regardless of what this function returns, a user cannot impersonate a
superuser, even if there are superusers in the returned QuerySet.

It is optional, and if it is not present, the user can impersonate any user
(i.e. the default is User.objects.all()).


    CUSTOM_ALLOW

A string that represents a function (e.g. 'module.submodule.mod.function_name')
that allows more fine grained control over who can use the impersonation. It
takes one argument, the request object, and should return True to allow
impesonation. Regardless of this setting, the user must be logged in to
impersonate. If this setting is used, REQUIRE_SUPERUSER is ignored.

It is optional, and if it is not present, the previous rules about superuser
and REQUIRE_SUPERUSER apply.


    REDIRECT_FIELD_NAME

A string that represents the name of a request (GET) parameter which contains
the URL to redirect to after impersonating a user. This can be used to redirect
to a custom page after impersonating a user. Example::

    # in settings.py
    IMPERSONATE = {'REDIRECT_FIELD_NAME': 'next'}

    # in your view
    <a href="{% url 'impersonate-list' %}?next=/some/url/">switch user</a>

To return always to the current page after impersonating a user, use request.path:

    ``<a href="{% url 'impersonate-list' %}?next={{request.path}}">switch user</a>``


    SEARCH_FIELDS

Array of user model fields used for building searching query. Default value is
[User.USERNAME_FIELD, 'first_name', 'last_name', 'email']. If the User model doesn't have
the USERNAME_FIELD attribute, it falls back to 'username' (< Django 1.5).


    LOOKUP_TYPE

A string that represents SQL lookup type for searching users by query on
fields above. It is 'icontains' by default.

    DISABLE_LOGGING

A bool that can be used to disable the logging of impersonation sessions. By
default each impersonation ``session_begin`` signal will create a new
``ImpersonationLog`` object, which is closed out (duration calculated) at
the corresponding ``session_end`` signal.

It is optional, and defaults to False (i.e. logging is enabled).

    MAX_FILTER_SIZE

The max number of items acceptable in the admin list filters. If the number of
items exceeds this, then the filter is removed (just shows all). This is used
by the "Filter by impersonator" filter.

It is optional, and defaults to 100.

SETTINGS PRIOR TO VERSION 1.3
=============================

Prior to version 1.3, settings were not stored in a dictionary. They were each an individual setting. For the time being, you can still use individual settings for each option. If present, they will supersede any setting within the ``IMPERSONATE`` dictionary and will also issue a warning that the settings format has changed and you should convert your projects settings to use the new dictionary format.

All dictionary options can be used as individual settings by simply prepending ``IMPERSONATE_`` to the name. For example, the following is the dictionary sample from above and it's old style settings equivalent.

New format::

    IMPERSONATE = {
        'REDIRECT_URL': '/some-path/',
        'PAGINATE_COUNT': 10,
    }


Deprecated (old) format::

    IMPERSONATE_REDIRECT_URL = '/some-path'
    IMPERSONATE_PAGE_COUNT = 10

Admin
=====

As of version 1.3 django-impersonate now includes a helper admin mixin, located at ``imepersonate.admin.UserAdminImpersonateMixin``, to include in your User model's ModelAdmin. This provides a direct link to impersonate users from your user model's Django admin list view. Using it is very simple, however if you're using the default ``django.contrib.auth.models.User`` model you will need to unregister the old ModelAdmin before registering your own.

The ``UserAdminImpersonateMixin`` has a attribute named ``open_new_window`` that **defaults to False**. If this is set to True a new window will be opened to start the new impersonation session when clicking the impersonate link directly in the admin.

Here's an example::

    # yourapp/admin.py
    from django.contrib import admin
    from django.contrib.auth.models import User
    from django.contrib.auth.admin import UserAdmin
    from impersonate.admin import UserAdminImpersonateMixin


    class NewUserAdmin(UserAdminImpersonateMixin, UserAdmin):
        open_new_window = True
        pass

    admin.site.unregister(User)
    admin.site.register(User, NewUserAdmin)

Testing
=======

You need factory_boy installed for tests to run. To install, use::

    $ pip install factory_boy

**Note:** This is currently not required for Python 3.3+. For more info on factory_boy, see: https://github.com/dnerdy/factory_boy

From the repo checkout, ensure you have Django in your PYTHONPATH and  run::

    $ python runtests.py

To get test coverage, use::

    $ coverage run --branch runtests.py
    $ coverage html  <- Pretty HTML files for you
    $ coverage report -m  <- Ascii report

If you're bored and want to test all the supported environments, you'll need tox.::

    $ pip install tox
    $ tox

And you should see::

    py3.6-django2.0: commands succeeded
    py3.6-django1.11: commands succeeded
    py3.5-django1.11: commands succeeded
    py3.5-django1.10: commands succeeded
    py3.5-django1.9: commands succeeded
    py3.5-django1.8: commands succeeded
    py3.4-django1.11: commands succeeded
    py3.4-django1.10: commands succeeded
    py3.4-django1.9: commands succeeded
    py3.4-django1.8: commands succeeded
    py3.3-django1.8: commands succeeded
    py2.7-django1.11: commands succeeded
    py2.7-django1.10: commands succeeded
    py2.7-django1.9: commands succeeded
    py2.7-django1.8: commands succeeded
    congratulations :)


Copyright & Warranty
====================
All documentation, libraries, and sample code are
Copyright 2011 Peter Sanchez <petersanchez@gmail.com>. The library and
sample code are made available to you under the terms of the BSD license
which is contained in the included file, BSD-LICENSE.


==================
Commercial Support
==================

This software, and lots of other software like it, has been built in support of many of
Netlandish's own projects, and the projects of our clients. We would love to help you
on your next project so get in touch by dropping us a note at hello@netlandish.com.
