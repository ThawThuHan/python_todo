# Use an official node runtime as a parent image
FROM node:16-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

ENV BACKEND_URL http://192.168.10.129:5000

RUN chmod +x /app/entrypoint.sh

# Install http-server to serve static files
RUN npm install -g http-server

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run http-server when the container launches
ENTRYPOINT [ "/app/entrypoint.sh" ]
