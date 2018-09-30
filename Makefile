COMPOSE_FILES :=  -f local.yml
IMAGE_NAME := benovatetestproject_django_1


build:
	docker-compose $(COMPOSE_FILES) build

up:
	docker-compose $(COMPOSE_FILES) up

start:
	docker-compose $(COMPOSE_FILES) start

create_admin:
	 docker exec -ti $(IMAGE_NAME) ./manage.py createsuperuser

get_in:
	docker exec -ti $(IMAGE_NAME) /bin/ash

down:
	docker-compose $(COMPOSE_FILES) down

test:
	 docker exec -ti $(IMAGE_NAME) pytest

debug:
	docker rm benovate_django_1
	docker-compose $(COMPOSE_FILES) run --name benovate_django_1 --service-ports django




