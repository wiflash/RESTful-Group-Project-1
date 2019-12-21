#!/usr/bin/env bash

clear
export FLASK_ENV="development"
export THIS_UNAME="root" # ganti ke username mysql
export THIS_PWD="" # ganti ke password mysql
export THIS_DB_TEST="restful_group_project_test" # ganti ke nama database yang dipake untuk unit testing
export THIS_DB_DEV="restful_group_project" # ganti ke nama database yang dipake untuk development

mysql --user=$THIS_UNAME --password=$THIS_PWD -e "create database if not exists $THIS_DB_DEV; create database if not exists $THIS_DB_TEST"

python app.py db init
python app.py db migrate
python app.py db upgrade
python app.py