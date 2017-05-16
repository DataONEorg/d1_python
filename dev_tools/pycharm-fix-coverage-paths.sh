#!/usr/bin/env bash

# PyCharm can't resolve the relative paths written by pytest's coverage plugin.
# This converts them to absolute, which PyCharm handles.

sed 's/filename="\([^"]*\)"/filename="\~\/d1-git\/d1_python\/\1"/g' coverage.xml > coverage_fixed.xml
