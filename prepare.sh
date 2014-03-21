#!/bin/bash

virtualenv -p `which python2` --no-site-packages .
source bin/activate
pip install -r requirements.txt
export DATABASE_URL="sqlite://database.sqlite"
foreman start -f Procfile_dev
