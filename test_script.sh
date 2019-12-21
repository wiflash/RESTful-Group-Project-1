#!/usr/bin/env bash

clear
export FLASK_ENV=testing
export THIS_UNAME="root" # ganti ke username mysql
export THIS_PWD="" # ganti ke password mysql
export THIS_DB_TEST="restful_group_project_test" # ganti ke nama database yang dipake untuk unit testing
export THIS_DB_DEV="restful_group_project" # ganti ke nama database yang dipake untuk development

mysql --user=$THIS_UNAME --password=$THIS_PWD -e "create database if not exists $THIS_DB_DEV; create database if not exists $THIS_DB_TEST"

pytest --cov-fail-under=80 --cov=blueprints --cov-report html -s tests/
export FLASK_ENV=development