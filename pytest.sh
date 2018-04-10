#!/usr/bin/env bash

pytest --skip-clear
pytest -n auto --reuse-db --cov=. --cov-report=term --cov-report=xml
pytest --skip -vvv --capture=no --exitfirst --reuse-db --sample-ask --pycharm
