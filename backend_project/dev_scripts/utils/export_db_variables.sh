#!/bin/bash

# run the script after running the init_test_envrionnement.sh script or a docker-compose up
# use source or . to run the script

DB_SERVICE_NAME="backend-project-db"


# Export DB_HOST based on the Docker container's IP address
DB_HOST=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $DB_SERVICE_NAME)
export DB_HOST=$DB_HOST

# Export the database credentials that you can get from backend_project/dev_scripts/docker/.env
export DB_USER="postgres_user"
export DB_PASSWORD="postgres_password"
export DB_NAME="postgres_dev"