export PORT=3000
export DB_HOST=':memory'
export REDIS_HOST='redis://localhost:6379'

celery -A octopus.jobs worker