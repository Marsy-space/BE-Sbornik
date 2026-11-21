# Архитектура в модели C4

Почему выбрана эта архитектура — [ADR-0002](../adr/ADR-0002-modular-monolith.md).

| Файл | Уровень | Что показывает |
| --- | --- | --- |
| [`c4-context.puml`](c4-context.puml) ([svg](c4-context.svg)) | 1. Контекст | Система одним блоком, роли (Guest, User, Admin) |
| [`c4-container.puml`](c4-container.puml) ([svg](c4-container.svg)) | 2. Контейнеры | Клиент, Сервер, База данных, Nginx |

Для создания диаграмм в VS Code можно использовать плагин PlantUML.
