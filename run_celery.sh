export PORT=3000
export DB_HOST='octopus.sqlite3'
export REDIS_HOST='redis://localhost:6379'
export SALT='it is salty'
export PRIVATE_KEY_FILE=dummy.key

celery -A octopus.jobs worker