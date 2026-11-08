# Развертывание и сетевое взаимодействие

## 1. Переменные окружения
Для запуска проекта в корне необходимо создать файл `.env` (пример есть в `.env.example`):
```env
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/recipes_db
SECRET_KEY=your_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
