# Makefile

# Load .env file if it exists
include .env
export $(shell sed 's/=.*//' .env)

build:
	docker build -t optimus0701/web_ai_server:latest .

build-fresh:
	docker build --no-cache -t optimus0701/web_ai_server:latest .

up:
	@if [ "$(ENVIRONMENT)" = "development" ]; then \
		printf "\033[1;33m🧪 Running in DEVELOPMENT mode...\033[0m\n"; \
		docker compose -f docker-compose.yml -f docker-compose.override.yml up; \
	else \
		printf "\033[0;37m🚀 Running in PRODUCTION mode...\033[0m\n"; \
		docker compose -f docker-compose.yml up -d; \
	fi

stop:
	docker compose down

down:
	docker compose down

logs:
	docker compose logs -f

push:
	docker push optimus0701/web_ai_server:latest
