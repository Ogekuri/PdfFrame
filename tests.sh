#!/bin/bash
# -*- coding: utf-8 -*-
# VERSION: 0.5.0
# AUTHORS: ogekuri

FULL_PATH=$(readlink -f "$0")
SCRIPT_PATH=$(dirname "$FULL_PATH")

# Run tests in 1 phase by default.
# Optional post-link validation can be enabled with RUN_POST_LINK_PHASE=1.
if [ "$#" -eq 0 ]; then
  set -- tests
fi

PYTHONPATH="${SCRIPT_PATH}/src:${PYTHONPATH}" \
    uv run --project "${SCRIPT_PATH}" pytest "$@"

rc=$?
if [ $rc -ne 0 ]; then
  exit $rc
fi

if [ "${RUN_POST_LINK_PHASE:-0}" = "1" ]; then
  echo "[tests.sh] Main test suite OK. Running post-link tests..."
  PYTHONPATH="${SCRIPT_PATH}/src:${PYTHONPATH}" \
    RUN_POST_LINK_TESTS=1 \
    uv run --project "${SCRIPT_PATH}" pytest "$@"
fi
