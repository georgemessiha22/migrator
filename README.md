# Migrator

<p align="center">
  <a href="https://hub.docker.com/r/georgemessiha22/migrator"><img src="https://github.com/georgemessiha22/migrator/actions/workflows/docker-publish.yml/badge.svg" alt="Migrator CI Status" /></a>
  <a herf="https://github.com/georgemessiha22/migrator/actions/workflows/release.yml"><image src="https://github.com/georgemessiha22/migrator/actions/workflows/release.yml/badge.svg" alt="release"/></a>
</p>

Aiming to create a sidecar to create databases for services. **It only meant for local development**

## Problem
Migrator can be used in local dev environment if you have something like monorepo or `dev` repo with many services but you want to apply principle of each service has it's own database.
it will be hard to manage and you will need to create the databases manually everytime you clone the `dev` repo. the goal is to play nice with docker.

## Usage
The way to use this repo is to clone or fork it for your local development.
you can check all commands in `Makefile`, but here is highlights:

- Create a new database with same User and password as database name; 
assuming your database name is the same as your service name

    ```shell
    make create service={serviceName}
    ```

- Migrate the changes

    ```shell
    make migrate
    ```

- to add more python packages

    ```shell
    make add package={package_name}
    ```

### Local dev environment

add *Migrator* service in your docker-compose file like:
```yaml
services:
  migrator:
    image: georgemessiha22/migrator:latest
    command: /bin/sh -c "while sleep 1000; do :; done"
    environment:
      - DATABASE_PASSWORD=main
      - DATABASE_NAME=main
      - DATABASE_USER=main
      - DATABASE_TYPE=postgresql
      - DATABASE_DOMAIN=postgres
      - DATABASE_PORT=5432
    volumes:
      - ./dev/migrations:/app/migrator/migrations
```

## TODO
- [ ] MySQL and MariaDB support
- [ ] support rollback commands
