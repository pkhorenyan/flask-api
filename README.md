This repository contains a Flask application that uses a PostgreSQL database in
a Docker container. This app and database will run in isolated containers, making
deployment and management easier.

### Requirements
<hr>

In order to run this app you are going to need Docker and Docker Compose

- Docker: [install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [install Docker Compose](https://docs.docker.com/compose/install/)

### Installation
<hr>

Clone this repo anywhere you want and move into the directory:

`git clone https://github.com/pkhorenyan/flask-api`

`cd flask-api`

### Build and launch
<hr>

Start Docker Compose:

`docker-compose up`

This command creates and starts Flask and PostgreSQL containers.

Application will be available at http://127.0.0.1:5000

Shutting down:

`docker-compose down`

PostgreSQL container is configured to store data in a Docker volume. This means that all
the data will remain intact between container restarts.


### Running app
<hr>

The purpose of this application is to connect to https://jservice.io/api/random and to retrieve
quiz questions.

There are a couple of ways to do it:

1. You can manually send POST request to endpoint https://127.0.0.1:5000/api/

`curl -i -X POST -H 'Content-Type: application/json' -d '{"questions_num": integer}' https://127.0.0.1:5000/api/`

2. In Postman go to "Body" and then "raw". Choose JSON format and paste this:

```json
{
    "questions_num": integer
}
```
integer is a number of questions you would like to retrieve

First time you send POST request you'll get an empty JSON object but on the next request you'll
get previous number of questions. All questions are being added to the database.


