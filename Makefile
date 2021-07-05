PROJECT_NAME = orchestrapy
VERSION := $(shell cat VERSION)

run:
	@echo "[*] Running $(PROJECT_NAME)..."
	pipenv run python manage.py runserver

lint:
	@echo "[*] Linter $(PROJECT_NAME)..."
	pipenv run pylint containers app apis clients core files images networks owners projects servers services webhooks

test:
	@echo "[*] Tests $(PROJECT_NAME)..."
	pipenv run python manage.py test