
install:
	uv sync

migrate:
	uv run python3 manage.py migrate

dev:
	uv run python3 manage.py runserver

shell:
	uv run python3 manage.py shell

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

PORT ?= 8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi