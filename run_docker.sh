#! /bin/bash

docker-compose -f local.yml run --name benovate_django --service-ports django
