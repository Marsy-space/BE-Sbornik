# Recipe box— Backend

##  Описание проекта

Серверная часть веб-платформы «Сборник рецептов» — сервиса для хранения, систематизации и поиска кулинарных рецептов с учётом пищевых ограничений.

Backend обеспечивает:
- регистрацию и аутентификацию (JWT);
- разграничение ролей (Guest, User, Admin);
- CRUD-операции с рецептами;
- поиск и фильтрацию;
- функцию исключения продукта (аллергии);
- избранное и приватность рецептов.

##   Стек технологий

 Категория | Технология |
 Язык: TypeScript
 Фреймворк: React
 Стили: Tailwind CSS
 UI-компоненты: shadcn/ui
 Backend: Python (FastAPI)
 Архитектура: Monolith
 Контейнеризация: Docker, Docker Compose

##  Роли пользователей и варианты использования

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

###   Диаграмма вариантов использования

Use Case Diagram
<img width="787" height="991" alt="UseCase-Sbornik-Retseptov" src="https://github.com/user-attachments/assets/f3327ca8-09d5-499a-b464-5f73413386f0" />


##   Схема базы данных (ER-диаграмма)
ER Diagram
<img width="1249" height="440" alt="ER-diagram" src="https://github.com/user-attachments/assets/f1a3aef8-d646-43cc-8e0d-1e521be57ecf" />


Основные сущности:
- users — пользователи (id, email, password_hash, role, created_at);
- recipes — рецепты (id, user_id, title, description, photo_url, category, cooking_time, is_private, created_at);
- ingredients — ингредиенты (id, name);
- recipe_ingredients — связь рецептов и ингредиентов (recipe_id, ingredient_id, amount);
- favorites — избранное (user_id, recipe_id);
- categories — категории блюд.


##  API

Полное описание API — в файле *в разработке*

### Основные эндпоинты

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | /api/auth/register | Регистрация |
| POST | /api/auth/login | Вход |
| GET | /api/recipes | Список рецептов |
| GET | /api/recipes/{id} | Рецепт по ID |
| POST | /api/recipes | Создать рецепт |
| PUT | /api/recipes/{id} | Обновить рецепт |
| DELETE | /api/recipes/{id} | Удалить рецепт |
| GET | /api/recipes/search | Поиск с фильтрами |
| POST | /api/favorites/{id} | Добавить в избранное |
| GET | /api/admin/users | Список пользователей (Admin) |

##  Запуск

`bash
git clone https://github.com/Marsy-space/BE-Sbornik.git
cd BE-Sbornik
docker-compose up --build
