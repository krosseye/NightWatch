#!/bin/bash

# Fail on errors.
set -e

# Source .bashrc to ensure environment variables are loaded
. ~/.bashrc

# Set working directory to /app unless SRCDIR env var is defined
WORKDIR=${SRCDIR:-/app}

# Change to the working directory
cd $WORKDIR

# Install the locked dependencies into the container's Python; uv's .venv is the host's (shared via the /app volume)
mkdir -p build
uv export --frozen --no-hashes --no-emit-project --output-file build/requirements.txt
pip3 install -r build/requirements.txt

# Run build.py if no arguments are passed to the entrypoint script
if [ -z "$@" ]; then
    python build.py
else
    exec "$@"
fi
