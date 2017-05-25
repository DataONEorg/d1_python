#!/usr/bin/env bash

find . \( -name '*.bak' -or -name '*.tmp' -or -name '*.swp' -or -name '*.pyc' -or -name '__pycache__' \) -print -delete
