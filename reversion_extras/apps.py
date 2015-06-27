# -*- coding: utf8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ReversionExtrasConfig(AppConfig):
    name = 'reversion_extras'
    verbose_name = _("Reversion Extras")
