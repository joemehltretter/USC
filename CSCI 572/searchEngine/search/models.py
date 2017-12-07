# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Item(models.Model):
  query = models.TextField(default = '')
  #rankSelector = models.TextField(default = '')  

