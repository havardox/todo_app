# Todo App

A RESTful API for a todo app. Powered by FastAPI.

## Installation

1. Install Docker: https://docs.docker.com/get-docker/
2. Check if your installation comes with Docker Compose with the command `docker compose` or `docker-compose`. If not, install Docker Compose here: https://docs.docker.com/compose/install/
3. Done

## Run
`docker compose -f docker-compose-dev.yml up`

## Swagger UI
Go to `http://0.0.0.0:8000/docs`. Authentication and authorization is [Resource Owner Password Credentials flow](https://datatracker.ietf.org/doc/html/rfc6749#section-4.3). Create a user with the `/auth/create/user` endpoint.
Then click the green "Authorize" button and enter your username and password.
