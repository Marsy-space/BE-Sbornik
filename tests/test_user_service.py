import pytest
from app.crud import user as crud_user
from app.schemas.user import UserCreate

# Модульные тесты

def test_create_user_success(db_session):
    # Успешное создание
    data = UserCreate(email="test@example.com", password="password123", username="Tester")
    user = crud_user.create_user(db_session, data)
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.username == "Tester"
    assert user.role_id == 2
    assert user.password_hash != "password123"

def test_get_user_by_email(db_session):
    # Поиск по email (исправлен пароль)
    data = UserCreate(email="findme@example.com", password="password123", username="Finder")
    crud_user.create_user(db_session, data)
    
    found = crud_user.get_user_by_email(db_session, "findme@example.com")
    assert found is not None
    assert found.email == "findme@example.com"

def test_get_user_by_email_not_found(db_session):
    # Поиск несуществующего email (негативный сценарий)
    found = crud_user.get_user_by_email(db_session, "nonexistent@example.com")
    assert found is None

def test_block_user(db_session):
    # Блокировка (исправлен пароль)
    data = UserCreate(email="block@example.com", password="password123", username="Blocker")
    user = crud_user.create_user(db_session, data)
    assert user.is_blocked is False
    
    blocked = crud_user.block_user(db_session, user.id)
    assert blocked.is_blocked is True

def test_get_user_by_id(db_session):
    # Поиск по ID
    data = UserCreate(email="byid@example.com", password="password123", username="ById")
    created = crud_user.create_user(db_session, data)
    
    found = crud_user.get_user(db_session, created.id)
    assert found is not None
    assert found.id == created.id

# Параметризованные тесты

@pytest.mark.parametrize("email, username, expected_role", [
    ("user1@test.com", "User1", 2),
    ("user2@test.com", "User2", 2),
    ("admin@test.com", "Admin", 2), # При регистрации всем дается роль User
])
def test_create_user_parameterized(db_session, email, username, expected_role):
    data = UserCreate(email=email, password="password123", username=username)
    user = crud_user.create_user(db_session, data)
    
    assert user.email == email
    assert user.username == username
    assert user.role_id == expected_role