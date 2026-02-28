#!/bin/bash
# -*- coding: utf-8 -*-
# VERSION: 0.4.0
# AUTHORS: ogekuri

FULL_PATH=$(readlink -f "$0")
SCRIPT_PATH=$(dirname "$FULL_PATH")

exec uv run --project "${SCRIPT_PATH}" pdfframe "$@"
