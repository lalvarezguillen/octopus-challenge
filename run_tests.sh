export DEBUGGING=1
export PORT=3000
export DB_HOST=localhost
export DB_NAME=octopus
export DB_PORT=3306
export DB_USER=root
export DB_PASS=root
export REDIS_HOST='redis://localhost:6379'
export SALT_FILE='./salt.txt'
export PRIVATE_KEY_FILE='./private.key'

pytest tests --cov=backend --cov-report term-missing -s