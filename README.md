# Entera Homework - Poverty Rates
This repo contains code to retrieve, transform, and load data from the US Census poverty data.

## Project Structure

The project contains 3 top-level folders:

### Backend

The backend folder holds the migration files for the Postgres Database, and a deployment yaml file that has some configuration (detailed below). The migrations are used by Flyway to construct the database -- migrations allow things like rollbacks, tracibility of changes to the DB, and recreating a DB locally for development.

There are 2 migrations currently, 1 to create the table for zipcode data and a second containing a view. The view allows us to change the logic without moving data around.

### Kubernetes

The kubernetes folder contains a helm chart, which will deploy a Postgres database, an "init" container which installs Flyway and applies the above migrations, and a Postgraphile server which creates a GraphQL API layer on top of the database. This chart is from a personal project of mine, so the GraphQL came with for free :)

### Python

This contains the main code that extracts data from the US Census API, cleans it up, and loads into Postgres.

## Installing/Running

### Postgres Database
To run the postgres DB / helm chart, you'll need to install a "kind" cluster, kubectl, docker,  and helm locally. Once you have these installed, you can use the Makefile in this root to:

`make build-backend` will build the Flyway docker image and push to the kind cluster

`make upgrade-backend` will deploy postgres + flyway + postgraphile to the kind cluster. This will apply the migrations defined above.

Finally, you'll want to expose the service/port running Postgres to your local environment using
`make forward`

### Python Scripts

To run the python scripts, it is recommended to create a virtualenv, then install the requirements.txt file inside the `python/` folder.

You will need to request an API key from the US Census, and set it using 
`export US_CENSUS_API_KEY=<insert API Key>`

Assuming the Postgres database is ready, you can run `python python/src/main.py` to run the program. This will download the data, transform it, and load into Postgres.