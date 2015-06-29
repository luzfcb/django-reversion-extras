#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-reversion-extras
------------

Tests for `django-reversion-extras` views module.
"""

import os
import shutil
import unittest

THIS = os.path.dirname(__file__)
PARENT_OF_THIS = os.path.dirname(os.path.dirname(__file__))
print(PARENT_OF_THIS)
print(THIS)


from reversion_extras import views


class TestReversion_extras(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        pass

    def tearDown(self):
        pass

    def test_fail(self):
        assert 0 == 1

