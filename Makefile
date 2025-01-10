PROJECT_NAME = orchestrapy
VERSION := $(shell cat VERSION)

run:
	@echo "[*] Running $(PROJECT_NAME)...v$(VERSION)"
	docker compose up -d
	pipenv run python manage.py runserver

test:
	@echo "[*] Tests on $(PROJECT_NAME)...v$(VERSION)"
	pipenv run python manage.py test

migrate:
	@echo "[*] Migrating DB on $(PROJECT_NAME)..."
	pipenv run python manage.py migrate

makemigrations:
	@echo "[*] Creating migrations on $(PROJECT_NAME)..."
	pipenv run python manage.py makemigrations