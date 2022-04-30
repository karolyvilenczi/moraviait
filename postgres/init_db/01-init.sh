#!/bin/bash
set -e
export PGPASSWORD=$POSTGRES_PASSWORD;
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE USER $APP_DB_USER WITH PASSWORD '$APP_DB_PASS';
  CREATE DATABASE $APP_DB_NAME;
  GRANT ALL PRIVILEGES ON DATABASE $APP_DB_NAME TO $APP_DB_USER;
  \connect $APP_DB_NAME $APP_DB_USER
EOSQL


  # Goes after '\connect'
  # BEGIN;
  #   CREATE TABLE IF NOT EXISTS event (
	#   id CHAR(26) NOT NULL, 
  #   name varchar(20) not null	  
	# );	
  # COMMIT;