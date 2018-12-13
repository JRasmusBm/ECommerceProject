# Installation

## Prerequisites

* `pipenv`
* `docker`
* `docker-compose`

## Setup

1.  Clone the repository
2.  Run `docker-compose build`

## Deploy

3.  Run `docker-compose down; docker-compose up -d`
4.  Add the schema to the database
    1. Enter the docker container with `docker exec -t -i berriesandgoods bash`
    2. `cd` into `berriesandgoods/`
    3. Run `python manage.py migrate`
    4. Run the contents of `default.sql` against the database
5. Open up `localhost` to see the application.

# Background

This is the repository for our project in the course D0018E, Database
Technology, at Luleå University of Technology.

We open source it, as our project is now complete, and we do not see that
anyone will be able to plagiarize our work without other people being able to
trace it back to us.

We hope that it can be useful as a learning resource for other people.
