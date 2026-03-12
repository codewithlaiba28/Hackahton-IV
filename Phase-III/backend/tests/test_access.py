"""
Tests for access control endpoints.
Tests freemium gate enforcement.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status

from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_check_access_free_chapter_free_user(
    client: AsyncClient,
    free_user: User,
    sample_chapters: list,
    headers_free_user: dict
):
    """Test free user has access to free chapter."""
    response = await client.get(
        "/access/check?resource_type=chapter&resource_id=ch-001",
        headers=headers_free_user
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"]["has_access"] == True
    assert data["data"]["upgrade_required"] == False


@pytest.mark.asyncio
async def test_check_access_premium_chapter_free_user(
    client: AsyncClient,
    free_user: User,
    sample_chapters: list,
    headers_free_user: dict
):
    """Test free user does NOT have access to premium chapter."""
    response = await client.get(
        "/access/check?resource_type=chapter&resource_id=ch-004",
        headers=headers_free_user
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"]["has_access"] == False
    assert data["data"]["upgrade_required"] == True
    assert "premium" in data["data"]["reason"].lower()


@pytest.mark.asyncio
async def test_check_access_premium_chapter_premium_user(
    client: AsyncClient,
    premium_user: User,
    sample_chapters: list,
    headers_premium_user: dict
):
    """Test premium user has access to premium chapter."""
    response = await client.get(
        "/access/check?resource_type=chapter&resource_id=ch-004",
        headers=headers_premium_user
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"]["has_access"] == True
    assert data["data"]["upgrade_required"] == False


@pytest.mark.asyncio
async def test_check_access_nonexistent_chapter(
    client: AsyncClient,
    free_user: User,
    headers_free_user: dict
):
    """Test 404 for nonexistent chapter."""
    response = await client.get(
        "/access/check?resource_type=chapter&resource_id=ch-999",
        headers=headers_free_user
    )
    
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_check_access_unsupported_resource_type(
    client: AsyncClient,
    free_user: User,
    headers_free_user: dict
):
    """Test 400 for unsupported resource type."""
    response = await client.get(
        "/access/check?resource_type=quiz&resource_id=q-001",
        headers=headers_free_user
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_get_current_user_free(
    client: AsyncClient,
    free_user: User,
    headers_free_user: dict
):
    """Test getting current user info (free tier)."""
    response = await client.get("/users/me", headers=headers_free_user)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"]["email"] == free_user.email
    assert data["data"]["tier"] == "free"
    # API key should NEVER be returned
    assert "api_key" not in data["data"]


@pytest.mark.asyncio
async def test_get_current_user_premium(
    client: AsyncClient,
    premium_user: User,
    headers_premium_user: dict
):
    """Test getting current user info (premium tier)."""
    response = await client.get("/users/me", headers=headers_premium_user)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"]["email"] == premium_user.email
    assert data["data"]["tier"] == "premium"
    assert "api_key" not in data["data"]


@pytest.mark.asyncio
async def test_unauthenticated_access_check(
    client: AsyncClient
):
    """Test unauthenticated user gets 401 for access check."""
    response = await client.get("/access/check?resource_type=chapter&resource_id=ch-001")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_unauthenticated_user_info(
    client: AsyncClient
):
    """Test unauthenticated user gets 401 for user info."""
    response = await client.get("/users/me")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
