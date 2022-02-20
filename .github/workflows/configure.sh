#!/bin/bash

if [[ -n "$TEST_PASSWORD" && -n "$TEST_USERNAME" ]]; then
    ( \
        echo "[DEFAULT]" && \
        echo "username = $TEST_USERNAME" && \
        echo "password = $TEST_PASSWORD" && \
        echo -e "client_id = bmATbhsh9RH7QXAR3n9Z88GBRoVqyxktj1RXcs9I\nclient_secret = eAeq0D4CB9akF9WNpYZmYk8ZfrtpqfTV5TuerNa006dR5BdcYrMxnBPAN4Y2m9B4NR3DIT0w3A1BqlJIOZXyIa8M32kIsg2q85HxsnWit5nYyHv9CeZafk5NLtww7iNq";
    ) >> ./test_config.cfg
fi