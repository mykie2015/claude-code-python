---
name: python-testing
description: pytest patterns for Python projects. Use when writing tests, creating fixtures, or following TDD workflow.
---

# Python Testing Patterns

## When to Use
- Writing unit tests
- Creating test fixtures
- Following TDD approach
- Mocking external dependencies

## Test Structure

```python
# tests/test_user_service.py
import pytest
from unittest.mock import Mock
from src.services.user_service import UserService

@pytest.fixture
def user_service():
    return UserService()

@pytest.fixture
def mock_repo():
    return Mock()

class TestUserService:
    def test_get_user_by_id(self, user_service, mock_repo):
        # Arrange
        user_service.repository = mock_repo
        mock_repo.get_by_id.return_value = {"id": 1, "name": "John"}
        
        # Act
        result = user_service.get_user_by_id(1)
        
        # Assert
        assert result["name"] == "John"
        mock_repo.get_by_id.assert_called_once_with(1)
    
    def test_create_user_validates_input(self, user_service):
        with pytest.raises(ValueError):
            user_service.create_user({"name": ""})  # Empty name
```

## Fixtures

```python
# tests/conftest.py
import pytest
from unittest.mock import MagicMock
from src.db.session import AsyncSession

@pytest.fixture
def mock_db_session():
    return MagicMock(spec=AsyncSession)

@pytest.fixture
def sample_user():
    return {
        "id": 1,
        "email": "test@example.com",
        "name": "Test User"
    }
```

## Async Tests

```python
import pytest
from src.services.async_service import AsyncService

@pytest.mark.asyncio
async def test_async_fetch(async_service, httpx_mock):
    httpx_mock.add_response(json={"data": "test"})
    
    result = await async_service.fetch_data()
    assert result["data"] == "test"
```

## Mocking

```python
from unittest.mock import patch, MagicMock

def test_with_patch():
    with patch("src.services.user_service.Repository") as mock_repo_class:
        mock_repo = MagicMock()
        mock_repo_class.return_value = mock_repo
        
        service = UserService()
        result = service.get_user(1)
        
        assert mock_repo.get_by_id.called
```

## Best Practices
- Test one thing per test
- Use descriptive test names: `test_{function}_{scenario}`
- AAA pattern: Arrange, Act, Assert
- Use factories for complex test data
