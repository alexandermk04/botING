#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Decode the base64 string back into a JSON file
echo "$FIREBASE_ADMIN_B64" | base64 -d > boting-firebase-admin.json