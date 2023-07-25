#!/usr/bin/env make
.PHONY: migrator-build

include dev/help.mk

### Migrator

## build migrator
build:
	docker compose build

## run migrations.
migrate:
	docker compose run --rm migrator

## install new package using `package={package_name}`
add:
	docker compose run --rm migrator poetry add $(package)

## install new dev package using `package={package_name}`
add-dev:
	docker compose run --rm migrator poetry add --group dev $(package)

## create migration file
create:
	docker compose run --rm migrator python3 migrator/manage.py create $(service)

## format the project using `black`
format:
	docker compose run --rm migrator python3 black migrator
