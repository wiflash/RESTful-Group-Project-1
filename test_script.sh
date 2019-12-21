#!/usr/bin/env bash

clear
export FLASK_ENV=testing
pytest --cov-fail-under=80 --cov=blueprints --cov-report html -s tests/
export FLASK_ENV=development