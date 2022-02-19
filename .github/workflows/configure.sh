#!/bin/bash

if [[ -n "$TEST_PASSWORD" && -n "$TEST_USERNAME" ]]; then
    ( \
        echo "[DEFAULT]" && \
        echo "username = $TEST_USERNAME" && \
        echo "password = $TEST_PASSWORD";
    ) >> ./test_config.cfg
fi