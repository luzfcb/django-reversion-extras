# -*- coding: utf8 -*-
__author__ = 'luzfcb'
import os
import sys

THIS = os.path.dirname(__file__)
PARENT_OF_THIS = os.path.dirname(os.path.dirname(__file__))

sys.path.append(PARENT_OF_THIS)
sys.path.append(THIS)

print(PARENT_OF_THIS)
print(THIS)

