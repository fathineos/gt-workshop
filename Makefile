USER_ID?=$$(id -u)
GROUP_ID?=$$(id -g)

IMAGE_BASE_NAME=gt
IMAGE_TARGET_STAGE=development
IMAGE_TARGET_TAG=development

build:
	DOCKER_BUILDKIT=1 docker build . \
		-f docker/Dockerfile \
		--progress plain \
		--build-arg USER_ID=${USER_ID} \
		--build-arg GROUP_ID=${GROUP_ID} \
		--target ${IMAGE_TARGET_STAGE} \
		-t ${IMAGE_BASE_NAME}:${IMAGE_TARGET_TAG}

shell:
	docker-compose \
		-f docker-compose.yml \
		-f docker-compose.dev.yml \
		run --rm \
		gt-web bash

django-shell:
	docker-compose \
		-f docker-compose.yml \
		-f docker-compose.dev.yml \
		run --rm \
		--entrypoint="sh -c" \
		gt-web \
		"./manage.py shell"

db-shell:
	docker-compose \
		-f docker-compose.yml \
		-f docker-compose.dev.yml \
		run --rm \
		--entrypoint="sh -c" \
		gt-web \
		"./manage.py dbshell"

up: _bootstrap
	docker-compose \
		-f docker-compose.yml \
		-f docker-compose.dev.yml \
		-f docker-compose.override.yml \
		up \
		gt-nginx \
		gt-web \
		gt-postgres

_bootstrap: _create-override db-migrate

_create-override:
	if [ ! -f "docker-compose.override.yml" ]; \
		then echo 'version: "3.7"' >  docker-compose.override.yml; \
	fi

db-migrate:
	docker-compose \
		-f docker-compose.yml \
		-f docker-compose.dev.yml \
		run --rm \
		--entrypoint="sh -c" \
		gt-web \
		"sh /wait-for.sh -t 20 gt-postgres:5432 -- ./manage.py migrate"

stop:
	docker-compose \
		-f docker-compose.yml \
		-f docker-compose.dev.yml \
		-f docker-compose.override.yml \
		stop

down:
	docker-compose
		-f docker-compose.yml \
		-f docker-compose.dev.yml \
		down

test: _precommit
