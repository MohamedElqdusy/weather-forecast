# README

## System Requirements
( Python 3, Pip, Pipenv)

# Run locally
## 1- Install all the dependencies:
`$  pipenv install`

## 2- Activate this project's virtualenv
`$ pipenv shell`
## 3- Run the service:
`$ python3 manage.py runserver 8080`

# Tests
`$ python3 manage.py test`

# usage
##### End points:
- `http://localhost:8080/ping` A simple health check
- `http://localhost:8080/forecast/<city>` GET the current weather for a specific city
- `http://localhost:8080/forecast/<city>/at=datetime` GET the weather forecast for a specific date or datetime

# TODO
- #### Run `$ docker-compose up`
