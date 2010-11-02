#!/bin/bash

python manage.py sql athaliana
python manage.py syncdb
python batch_loader.py
