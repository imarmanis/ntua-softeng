#!/bin/bash

# Install dependencies
npm install
# Build
npm run build
# Run the server (NOT in the background, so we can kill it with a simple CTR-C)
npx serve -s dist
