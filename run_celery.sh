export PORT=3000
export DB_HOST='root:root@172.17.0.2:3306'
export REDIS_HOST='redis://localhost:6379'
export SALT='it is salty'
export PRIVATE_KEY_FILE=dummy.key

celery -A run_celery.CELERY worker