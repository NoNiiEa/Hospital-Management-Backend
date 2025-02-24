#!/bin/bash

# Default values
DEFAULT_IMAGE_NAME="my_project"
DEFAULT_PORT="8000"

# Prompt user for image name (or use default)
read -p "Enter image name (default: $DEFAULT_IMAGE_NAME): " IMAGE_NAME
IMAGE_NAME=${IMAGE_NAME:-$DEFAULT_IMAGE_NAME}

# Prompt user for port (or use default)
read -p "Enter port (default: $DEFAULT_PORT): " PORT
PORT=${PORT:-$DEFAULT_PORT}

# Build the Docker image
echo "Building Docker image: $IMAGE_NAME..."
docker build -t $IMAGE_NAME .

# Run the container with the specified port
echo "Starting the container..."
docker run -d -p $PORT:8000 --name "$IMAGE_NAME-container" $IMAGE_NAME

# Show running containers
docker ps
