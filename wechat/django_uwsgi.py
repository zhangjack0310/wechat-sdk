#!/usr/bin/env python
# coding: utf-8

import os
import sys

from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = 'wechat.settings'

application = get_wsgi_application()