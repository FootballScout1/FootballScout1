#!/bin/bash

if [ "$1" == "dev" ]; then
    export FOOTBALL_SCOUT_ENV=dev
    echo "Switched to dev environment"
elif [ "$1" == "test" ]; then
    export FOOTBALL_SCOUT_ENV=test
    echo "Switched to test environment"
else
    echo "Usage: $0 [dev|test]"
    exit 1
fi

source .env
# echo "Switched to $FOOTBALL_SCOUT_ENV environment"

