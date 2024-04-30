./bootstrap.sh
docker compose build
docker compose -f docker-compose.prod.yml up -d
docker compose logs