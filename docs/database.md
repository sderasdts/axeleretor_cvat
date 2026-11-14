# PostgreSQL в Docker

## Команды (запускать из корня проекта)

```bash
# 0. Один раз: создать файл с настройками
cp .env.example .env

# 1. Собрать и запустить всё в фоне
docker compose up -d --build

# 2. Посмотреть статус: у db должно быть (healthy), у обоих Up
docker compose ps

# 3. Проверить подключение backend → БД
docker compose exec backend python manage.py check_db
#   ожидаемый вывод:  OK: подключение к БД работает

# Логи backend (Ctrl+C — выйти из просмотра)
docker compose logs -f backend

# Создать админа для /admin/
docker compose exec backend python manage.py createsuperuser

# Открыть консоль PostgreSQL (выход — \q)
docker compose exec db psql -U ppe -d ppe

# Посмотреть, какие контейнеры подключены к сети
docker network inspect ppe-net

# Остановить (данные сохранятся)
docker compose down

# Остановить и УДАЛИТЬ ВСЕ ДАННЫЕ БД (база будет создана заново)
docker compose down -v
```

После изменения `requirements.txt` или `Dockerfile` пересобери образ: `docker compose up -d --build`.

## Запуск backend без Docker (только база в Docker)

```bash
docker compose up -d db          # поднимаем только базу
cd backend
python manage.py migrate
python manage.py runserver
```
В `.env` при этом должны быть `DB_HOST=localhost` и `DB_PORT=5433`, как в `.env.example`.

## Если что-то не работает

| Симптом | Причина и решение |
|---|---|
| `connection refused` / `could not connect` из backend в Docker | Проверь, что в `docker-compose.yml` у backend стоит `DB_HOST: db`, а не `localhost`. Ещё проверь, что `docker compose ps` показывает у db статус `healthy`. |
| `could not connect` при локальном `runserver` | В `.env` должен быть порт `5433`, а не `5432`. |
| `port is already allocated` при запуске | Порт 5433 или 8000 уже кто-то занял. Поменяй `DB_HOST_PORT` в `.env` или левую часть `"8000:8000"`. |
| `password authentication failed` после смены пароля в `.env` | Postgres задаёт пароль **только при первом создании** тома. Либо удали данные (`docker compose down -v`), либо смени пароль через `psql`: `ALTER USER ppe PASSWORD '...'`. |
| `Invalid HTTP_HOST header` | Добавь этот хост в `ALLOWED_HOSTS` в `.env`. |
