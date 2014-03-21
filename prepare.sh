#!/bin/bash

virtualenv -p `which python2` --no-site-packages .
pip -r requirements.txt
export DATABASE_URL="sqlite://database.sqlite"
foreman start -p Procfile_dev
