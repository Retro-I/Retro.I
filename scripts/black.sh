#!/bin/bash
set -e

# Run black inside the venv, passing all arguments
black . --line-length 80 --exclude '.\.venv' "$@"
