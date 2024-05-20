# Use an official node runtime as a parent image
FROM node:16-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

ENV BACKEND_HOST 192.168.10.129
ENV BACKEND_PORT 5000

RUN sed -i "s/127.0.0.1:5000/$BACKEND_HOST:$BACKEND_PORT/g" /app/script.js

# Install http-server to serve static files
RUN npm install -g http-server

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run http-server when the container launches
CMD ["http-server", "-p", "8080"]
