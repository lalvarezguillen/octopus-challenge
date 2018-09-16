export DEBUGGING=1
export PORT=3000
export DB_HOST=localhost
export DB_NAME=octopus
export DB_PORT=3306
export DB_USER=root
export DB_PASS=root
export REDIS_HOST='redis://localhost:6379'
export SALT=salt.txt
export PRIVATE_KEY_FILE=private.key

celery -A run_celery.CELERY worker --loglevel=info