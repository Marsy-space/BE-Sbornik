# Развертывание и сетевое взаимодействие

Документ описывает, как запустить систему «Сборник рецептов» с нуля.

## 1. Требования
| Что | Требование |
| --- | --- |
| ОС | macOS, Linux или Windows с WSL 2 |
| Docker | Docker с Compose v2 (Docker Desktop) |
| Порты | Свободен порт 8000 на компьютере |

## 2. Расположение репозиториев
```bash
git clone https://github.com/Marsy-space/BE-Sbornik.git
cd BE-Sbornik
```

## 3. Переменные окружения

Переменные задаются в `deploy/.env`. Файл не попадает в репозиторий (`.gitignore`); образец — [deploy/.env.example](../deploy/.env.example).

| Переменная | Назначение | Пример |
| --- | --- | --- |
| `DATABASE_URL` | Строка подключения к БД | `postgresql+psycopg2://postgres:password@db:5432/recipes_db` |
| `SECRET_KEY` | Секретный ключ для JWT | `your_super_secret_key` |

```bash
cd deploy
cp .env.example .env    # один раз; задайте свои значения
```

## 4. Запуск, проверка, остановка

```bash
docker compose up --build -d    # сборка и запуск в фоне
docker compose ps               # проверка статуса контейнеров
```

Проверка: откройте в браузере http://localhost:8000/docs. Должен открыться интерфейс Swagger UI.

Остановка:

```bash
docker compose down       # контейнеры удаляются, данные БД остаются
docker compose down -v    # УДАЛЯЕТ данные БД
```

## 5. Сервисы
| Сервис | Образ | Порт наружу | Зависит от |
| --- | --- | --- |
| `db` | `postgres:17` | — | — |
| `backend` | собирается из `Dockerfile` | 8000 | `db` |

## 6. Запуск выпущенной версии
Выпущенный релиз — это тег в Git. Поднять его без сборки:

```bash
git switch --detach v0.6.0
cd deploy
docker compose up --no-build -d
```

## 7. Типичные проблемы
| Симптом | Причина | Решение |
| --- | --- | --- |
| `port is already allocated` | Порт 8000 занят | Остановите другую программу или измените порт в `docker-compose.yml` |
| `password authentication failed` | Неверный пароль в `.env` | Проверьте `DATABASE_URL` в `.env` |
| Страница не открывается | Сервер не запустился | `docker compose logs backend` |