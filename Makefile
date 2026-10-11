.RECIPEPREFIX := >
COMPOSE ?= docker compose

up:
> $(COMPOSE) up -d --build

down:
> $(COMPOSE) down

logs:
> $(COMPOSE) logs -f

lint:
> flake8 app.py forms.py tests --max-line-length=120

test:
> pytest -v

backup:
> $(COMPOSE) exec -T db sh -c 'mysqldump -uroot -p"$$MYSQL_ROOT_PASSWORD" "$$MYSQL_DATABASE"' > backup.sql

scan:
> docker build -t tastybites-web .
> docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --severity HIGH,CRITICAL tastybites-web