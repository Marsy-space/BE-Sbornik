-- Групповой доступ к приватным рецептам (согласовать с Лерой, т.к. ссылаемся на ее таблицу recipes)
CREATE TABLE recipe_access (
    recipe_id INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (recipe_id, user_id)
);
