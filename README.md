## Генератор сайтов
# Quickstart

## Запуск

1. Скопировать `.env` с токеном PandaScore и URL сайта.
2. Собрать Docker-образы:

**Билд**
```bash
make docker-build
```

**Запуск контейнеров**
```bash
make docker-up
```

**Остановить контейнеры**
```bash
make docker-down
```
