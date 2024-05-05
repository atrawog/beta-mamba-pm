./bootstrap.sh

# TESTING

docker compose build
docker compose up -d
docker compose down
docker compose ps
docker compose logs
docker compose exec quetz bash

# PROD

#docker compose -f docker-compose.prod.yml --project-name beta-mamba-pm-prod build
docker compose -f docker-compose.prod.yml --project-name beta-mamba-pm-prod up -d
docker compose -f docker-compose.prod.yml --project-name beta-mamba-pm-prod down
docker compose -f docker-compose.prod.yml --project-name beta-mamba-pm-prod ps
docker compose -f docker-compose.prod.yml --project-name beta-mamba-pm-prod logs
docker compose -f docker-compose.prod.yml --project-name beta-mamba-pm-prod exec quetz bash

