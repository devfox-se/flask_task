migrate:
	docker-compose run --rm api_task flask db migrate

upgrade:
	docker-compose run --rm api_task flask db upgrade