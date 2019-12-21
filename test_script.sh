#!/usr/bin/env bash

clear
export FLASK_ENV="development"
export THIS_UNAME="root" # ganti ke username mysql
export THIS_PWD="" # ganti ke password mysql
export THIS_DB_TEST="restful_group_project_test" # ganti ke nama database yang dipake untuk unit testing
export THIS_DB_DEV="restful_group_project" # ganti ke nama database yang dipake untuk development

export FLASK_ENV=testing
pytest --cov-fail-under=80 --cov=blueprints --cov-report html -s tests/
export FLASK_ENV=development