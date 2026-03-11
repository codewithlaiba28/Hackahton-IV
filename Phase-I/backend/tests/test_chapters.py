"""
Tests for chapter endpoints.
Tests content delivery and navigation features.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status

from app.main import app
from app.models.user import UserTier


@pytest.fixture
def client():
    """Create test client."""
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_list_chapters_free_user(
    client: AsyncClient,
    free_user: User,
    sample_chapters: list,
    headers_free_user: dict
):
    """Test free user can list all chapters with is_locked flag."""
    response = await client.get("/chapters", headers=headers_free_user)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"]["chapters"]
    assert len(data["data"]["chapters"]) == 5
    
    # First 3 chapters should be unlocked
    for chapter in data["data"]["chapters"][:3]:
        assert chapter["is_locked"] == False
        assert chapter["is_free"] == True
    
    # Last 2 chapters should be locked for free user
    for chapter in data["data"]["chapters"][3:]:
        assert chapter["is_locked"] == True
        assert chapter["is_free"] == False


@pytest.mark.asyncio
async def test_list_chapters_premium_user(
    client: AsyncClient,
    premium_user: User,
    sample_chapters: list,
    headers_premium_user: dict
):
    """Test premium user sees all chapters unlocked."""
    response = await client.get("/chapters", headers=headers_premium_user)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # All chapters should be unlocked for premium user
    for chapter in data["data"]["chapters"]:
        assert chapter["is_locked"] == False


@pytest.mark.asyncio
async def test_get_free_chapter(
    client: AsyncClient,
    free_user: User,
    sample_chapters: list,
    headers_free_user: dict
):
    """Test free user can access free chapter content."""
    response = await client.get("/chapters/ch-001", headers=headers_free_user)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"]["id"] == "ch-001"
    assert data["data"]["title"] == "Introduction to AI Agents"
    assert data["data"]["is_locked"] == False


@pytest.mark.asyncio
async def test_get_premium_chapter_free_user(
    client: AsyncClient,
    free_user: User,
    sample_chapters: list,
    headers_free_user: dict
):
    """Test free user gets 403 for premium chapter."""
    response = await client.get("/chapters/ch-004", headers=headers_free_user)
    
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_get_premium_chapter_premium_user(
    client: AsyncClient,
    premium_user: User,
    sample_chapters: list,
    headers_premium_user: dict
):
    """Test premium user can access premium chapter."""
    response = await client.get("/chapters/ch-004", headers=headers_premium_user)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"]["id"] == "ch-004"
    assert data["data"]["is_locked"] == False


@pytest.mark.asyncio
async def test_get_nonexistent_chapter(
    client: AsyncClient,
    free_user: User,
    headers_free_user: dict
):
    """Test 404 for nonexistent chapter."""
    response = await client.get("/chapters/ch-999", headers=headers_free_user)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_next_chapter(
    client: AsyncClient,
    free_user: User,
    sample_chapters: list,
    headers_free_user: dict
):
    """Test navigation to next chapter."""
    response = await client.get("/chapters/ch-001/next", headers=headers_free_user)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"]["id"] == "ch-002"
    assert data["data"]["prev_chapter_id"] == "ch-001"


@pytest.mark.asyncio
async def test_get_prev_chapter(
    client: AsyncClient,
    free_user: User,
    sample_chapters: list,
    headers_free_user: dict
):
    """Test navigation to previous chapter."""
    response = await client.get("/chapters/ch-002/prev", headers=headers_free_user)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"]["id"] == "ch-001"
    assert data["data"]["next_chapter_id"] == "ch-002"


@pytest.mark.asyncio
async def test_first_chapter_no_prev(
    client: AsyncClient,
    free_user: User,
    sample_chapters: list,
    headers_free_user: dict
):
    """Test first chapter returns null for prev."""
    response = await client.get("/chapters/ch-001/prev", headers=headers_free_user)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"] is None


@pytest.mark.asyncio
async def test_last_chapter_no_next(
    client: AsyncClient,
    free_user: User,
    sample_chapters: list,
    headers_free_user: dict
):
    """Test last chapter returns null for next."""
    response = await client.get("/chapters/ch-005/next", headers=headers_free_user)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"] is None


@pytest.mark.asyncio
async def test_next_chapter_premium_free_user(
    client: AsyncClient,
    free_user: User,
    sample_chapters: list,
    headers_free_user: dict
):
    """Test free user gets 403 when next chapter is premium."""
    # ch-003's next is ch-004 (premium)
    response = await client.get("/chapters/ch-003/next", headers=headers_free_user)
    
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_unauthenticated_access(
    client: AsyncClient,
    sample_chapters: list
):
    """Test unauthenticated user gets 401."""
    response = await client.get("/chapters")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
