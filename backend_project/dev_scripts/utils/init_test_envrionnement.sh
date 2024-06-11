#!/bin/bash

# Define the path to your docker-compose file
COMPOSE_FILE_PATH="./dev_scripts/docker/docker-compose.yml"

# Define the name of your database service
DB_SERVICE_NAME="backend-project-db"

# Start the database service
docker-compose -f $COMPOSE_FILE_PATH up -d $DB_SERVICE_NAME

# Wait for the database to be ready
echo "Waiting for the database to be ready..."
until docker-compose -f $COMPOSE_FILE_PATH exec $DB_SERVICE_NAME pg_isready -U postgres; do
    sleep 1
done
echo "Database is now ready."

# Get the IP address of the db service container
DB_HOST=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker-compose -f $COMPOSE_FILE_PATH ps -q $DB_SERVICE_NAME))

# Write the IP address to a .local.env file
echo "DB_HOST=$DB_HOST" > dev_scripts/.local.env

echo "DB_HOST has been written to .local.env."