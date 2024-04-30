./bootstrap.sh
docker compose build
docker compose -f docker-compose.prod.yml up -d
docker compose logs

docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml --project-name beta-mamba-pm-prod up -d
docker compose -f docker-compose.prod.yml --project-name beta-mamba-pm-prod down
docker compose -f docker-compose.prod.yml --project-name beta-mamba-pm-prod ps
docker compose -f docker-compose.prod.yml --project-name beta-mamba-pm-prod logs
