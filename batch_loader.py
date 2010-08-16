#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from django.core.management import setup_environ
sys.path.append("/home/bao/public_html/")
from bao import settings
setup_environ(settings)

from bao.athaliana.models import Syntelog 

import csv
reader = csv.DictReader(open("/home/bao/public_html/appspot/data/data.csv"))
   
for i, row in enumerate(reader):
    if i % 1000 == 0: print >>sys.stderr, i, "records loaded"
    Syntelog.objects.get_or_create(**row)

