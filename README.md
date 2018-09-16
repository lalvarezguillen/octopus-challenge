# Octopuslabs Challenge

This is my solution to the technical challenge by Octopuslabs.

## Running the project

Running the project will spin up 4 docker containers:

* A Tornado web application
* A Celery worker that takes care of the asynchronous tasks that power this project
* A MySQL server to persist the application's data
* A Redis server to act as IPC vehicle between the web application and the Celery workers

The repo includes some throwaway settings by default.

Spin un up the containers with:

``` bash
docker-compose up
```

### Requirements:

* Docker >= 17.09.0
* Docker Compose >= 1.21.0

### Running with custom settings:

The project's configuration is set through environment variables. 

For more information about each of the configurable paramaters, read their documentation in backend/config.py


### Handling secrets securily

* Avoid including production/staging secrets in the repo
* Avoid including production/staging secrets in the container build
* Environment variables should be a non-terrible way to inject sensitive information when launching the services
* Docker Secrets should be the preferred alternative, if the infrastructure permits.

## Hacking on the project

In order to hack on the project you'd:

* Clone the repo
```sh
git clone https://github.com/lalvarezguillen/octopus-challenge
```

* Setup a virtual environment
```sh
virtualenv .env
```

* Install dependencies
```sh
pip install -r requirements.dist.txt -r requirements.dev.txt
```

* Run the tests to make sure everything is working. A bash script has been included for convenience:
``` sh
bash run_tests.sh
```

* Break things up

The project has been formatted with Black, and I've deferred every code styling decision to that library.

### Requirements

* Python >= 3.6
* MySQL


## TODO

* JS unittests
* Functional tests with Selenium