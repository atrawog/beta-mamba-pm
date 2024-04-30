./bootstrap.sh
docker compose build
docker compose -f docker-compose.prod.yml up -d
docker compose logs

docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs
