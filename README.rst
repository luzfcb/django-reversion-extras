=============================
django-reversion-extras
=============================

.. image:: https://img.shields.io/pypi/v/django-reversion-extras.svg
    :target: https://badge.fury.io/py/django-reversion-extras

.. image:: https://img.shields.io/pypi/status/django-reversion-extras.svg
    :target: https://badge.fury.io/py/django-reversion-extras

.. image:: https://travis-ci.org/luzfcb/django-reversion-extras.svg?branch=master
    :target: https://travis-ci.org/luzfcb/django-reversion-extras

.. image:: https://coveralls.io/repos/luzfcb/django-reversion-extras/badge.svg?branch=master
    :target: https://coveralls.io/r/luzfcb/django-reversion-extras?branch=master

.. image:: https://landscape.io/github/luzfcb/django-reversion-extras/master/landscape.svg?style=flat
    :target: https://landscape.io/github/luzfcb/django-reversion-extras/master
    :alt: Code Health

.. image:: https://requires.io/github/luzfcb/django-reversion-extras/requirements.svg?branch=master
    :target: https://requires.io/github/luzfcb/django-reversion-extras/requirements/?branch=master
    :alt: Requirements Status

.. image:: https://img.shields.io/pypi/dd//django-reversion-extras.svg
    :target: https://badge.fury.io/py/django-reversion-extras

.. image:: https://img.shields.io/pypi/dm//django-reversion-extras.svg
    :target: https://badge.fury.io/py/django-reversion-extras



Extra tools to work with django-reversion

.. DANGER::
   It is not ready for use, it does not have tests and only serves to try to validate the use of django-reversion for things which it was not designed

Documentation
-------------

The full documentation is at https://django-reversion-extras.readthedocs.org.

Quickstart
----------

Install django-reversion-extras::

    pip install django-reversion-extras

Then use it in a project::

    from reversion_extras.views import DetailVersionListView, UpdateVersionListView



``DetailVersionListView`` provides the same functionality as django.views.generic.DetailView

``UpdateVersionListView`` provides the same functionality as django.views.generic.UpdateView

All inject in the template context some new variables:

``object_versions_list``: contains the list of django-reversion Versions of current model instance. The same
value  returned from ``reversion.get_for_object(model_instance)``

``model_name_versions_list``: is a alias to object_versions_list

``version_paginator``
``version_page_obj``
``version_is_paginated``



Features
--------

* TODO:

Create ReversionView
Create CompareVersionView

