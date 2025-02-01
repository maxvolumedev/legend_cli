#!/bin/bash
# Script to provide git credentials from environment variables

case "$1" in
    *Username*) echo "$GIT_USERNAME" ;;
    *Password*) echo "$GIT_PASSWORD" ;;
esac
