#!/bin/sh

current_dir=$(pwd)
echo "Current directory: $current_dir"

# # Run the session controller script
# python spotify_module.py

exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"