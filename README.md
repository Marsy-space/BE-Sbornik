# Сборник рецептов — Backend

Серверная часть веб-платформы **«Сборник рецептов»** — сервиса для хранения, систематизации и поиска кулинарных рецептов с учётом пищевых ограничений.

Backend обеспечивает:
- регистрацию и аутентификацию (JWT);
- разграничение ролей (Guest, User, Admin);
- CRUD-операции с рецептами;
- поиск и фильтрацию;
- функцию исключения продукта (аллергии);
- избранное и приватность рецептов;
- WebSocket-чат.

## 🛠 Стек технологий

| Категория | Технология |
| :--- | :--- |
| **Язык** | Python 3.11 |
| **Фреймворк** | FastAPI |
| **ORM** | SQLAlchemy |
| **БД** | PostgreSQL |
| **Аутентификация** | JWT (JSON Web Tokens) |
| **Контейнеризация** | Docker, Docker Compose |

## 🚀 Запуск

Для полноценной работы приложения сначала поднимите БД и бэкенд по [инструкции запуска бэкенда](#запуск-бэкенда). Затем запустите фронтенд по [инструкции из репозитория фронтенда](https://github.com/polinastah/recipe_box_front#запуск-фронтенда).

### Запуск бэкенда

Выполните следующие команды для запуска серверной части:

1. Склонируйте репозиторий:
```bash
git clone https://github.com/Marsy-space/BE-Sbornik.git
cd BE-Sbornik
```
2. Перейдите в папку `deploy` и создайте файл `.env` из примера:
```bash
cd deploy
cp .env.example .env
```
3. Запустите контейнеры:
```bash
docker compose up --build -d
```
4. Проверьте работу: откройте в браузере http://localhost:8000/docs (Swagger UI).

Остановить проект: `docker compose down`.

## 📁 Структура проекта

| Папка | Содержимое |
| :--- | :--- |
| `app/` | Исходный код (API, модели, CRUD, схемы) |
| `docs/` | Документация проекта ([оглавление](./docs/README.md)) |
| `api/` | Контракт API (`openapi.yaml`) |
| `deploy/` | Docker Compose и переменные окружения |
| `sql/` | SQL-скрипты (если используются отдельно) |

## 🪪 Роли пользователей

### Guest (неавторизованный пользователь)
- просмотр общедоступных рецептов;
- поиск по ингредиентам и категориям;
- регистрация;
- подтверждение ознакомления с правилами.

### User (авторизованный пользователь)
- добавление, редактирование, удаление своих рецептов;
- загрузка фотографий;
- поиск с исключением аллергенов;
- фильтрация по категориям и времени;
- сохранение в избранное;
- настройка приватности рецептов.

### Admin (администратор)
- просмотр списка пользователей;
- контроль соблюдения авторских прав;
- просмотр статистики;
- блокировка пользователей.

## 📊 Диаграммы

### Use Case Diagram

<img width="787" height="991" alt="UseCase-Sbornik-Retseptov" src="https://github.com/user-attachments/assets/f3327ca8-09d5-499a-b464-5f73413386f0" />

### ER Diagram (Схема базы данных)

<img width="1249" height="440" alt="ER-diagram" src="https://github.com/user-attachments/assets/f1a3aef8-d646-43cc-8e0d-1e521be57ecf" />

Основные сущности:
- **users** — пользователи (id, email, password_hash, role, created_at);
- **recipes** — рецепты (id, user_id, title, description, photo_url, category, cooking_time, is_private, created_at);
- **ingredients** — ингредиенты (id, name);
- recipe_ingredients — связь рецептов и ингредиентов (recipe_id, ingredient_id, amount);
- **favorites** — избранное (user_id, recipe_id);
- **categories** — категории блюд.

## 📌 Основные эндпоинты API

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/auth/register` | Регистрация |
| POST | `/api/auth/login` | Вход |
| GET | `/api/recipes` | Список рецептов |
| GET | `/api/recipes/{id}` | Рецепт по ID |
| POST | `/api/recipes` | Создать рецепт |
| PUT | `/api/recipes/{id}` | Обновить рецепт |
| DELETE | `/api/recipes/{id}` | Удалить рецепт |
| GET | `/api/recipes/search` | Поиск с фильтрами |
| POST | `/api/favorites/{id}` | Добавить в избранное |
| GET | `/api/admin/users` | Список пользователей (Admin) |

*Полное описание всех эндпоинтов и форматов данных доступно в файле [openapi.yaml](./api/openapi.yaml) и в Swagger UI при запущенном сервере.*

## 📚 Документация и правила
- [Оглавление всей документации проекта](./docs/README.md)
- [Контракт API (OpenAPI)](./api/openapi.yaml)
- [Правила работы с репозиторием (CONTRIBUTING)](./CONTRIBUTING.md)

## ✅ Запуск тестов
Локальный запуск (если настроено виртуальное окружение):
```bash
pytest tests/ -v
```
Если тесты запускаются внутри Docker-контейнера:
```bash
docker compose exec backend pytest tests/ -v
```

## 👥 Команда проекта
* Морозова Ксения (Product Owner, Technical Writer, BE)
* Стахейко Полина (Тим-лид, Testing, FE)
* Борозна Диана (DevOps, FE)
* Шугар Валерия (UI, BE)