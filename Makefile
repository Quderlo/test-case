sync:
	uv sync --group debug

test:
	@echo "Запуск юнит-тестов..."
	uv run env PYTHONPATH=. python -m pytest --maxfail=1 --disable-warnings -v

docker-build:
	@echo "Сборка Docker-образа Flask..."
	docker compose build web

docker-up:
	@echo "Запуск контейнеров Flask + Nginx..."
	docker compose up -d

docker-down:
	@echo "Остановка контейнеров..."
	docker compose down

docker-logs:
	@echo "Логи всех контейнеров..."
	docker compose logs -f
