#!/usr/bin/env bash

find . \( -name '*.bak' -or -name '*.tmp' -or -name '*.swp' \) -print -delete

