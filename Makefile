
install:
	uv sync

migrate:
	uv run python3 manage.py migrate

start:
	uv run python3 manage.py runserver

shell:
	uv run python3 manage.py shell

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi