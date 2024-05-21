#!/bin/sh

# Replace the backend URL in script.js
sed -i "s|http://127.0.0.1:5000|$BACKEND_URL|g" /app/script.js

# Start http-server
http-server -p 8080