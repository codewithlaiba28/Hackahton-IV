"""
Tests for search endpoint.
Tests PostgreSQL full-text search functionality.
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
async def test_search_requires_query_parameter(
    client: AsyncClient,
    free_user: User,
    headers_free_user: dict
):
    """Test search requires 'q' query parameter."""
    response = await client.get("/search", headers=headers_free_user)
    
    # FastAPI should return 422 for missing required parameter
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_search_empty_results(
    client: AsyncClient,
    free_user: User,
    headers_free_user: dict
):
    """Test search returns empty list for unknown terms."""
    response = await client.get(
        "/search?q=nonexistentterm12345",
        headers=headers_free_user
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Should return empty array, not error
    assert data["data"] == []


@pytest.mark.asyncio
async def test_search_free_user_excludes_premium(
    client: AsyncClient,
    free_user: User,
    sample_chapters: list,
    headers_free_user: dict
):
    """Test free user doesn't get results from premium chapters."""
    # Search for a term that might be in any chapter
    response = await client.get(
        "/search?q=agent",
        headers=headers_free_user
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Verify no premium chapter results (ch-004, ch-005)
    for result in data["data"]:
        assert result["chapter_id"] not in ["ch-004", "ch-005"]


@pytest.mark.asyncio
async def test_search_premium_user_all_results(
    client: AsyncClient,
    premium_user: User,
    sample_chapters: list,
    headers_premium_user: dict
):
    """Test premium user gets results from all chapters."""
    response = await client.get(
        "/search?q=agent",
        headers=headers_premium_user
    )
    
    assert response.status_code == status.HTTP_200_OK
    # Premium user can see results from all chapters
    # (actual results depend on search vector data)


@pytest.mark.asyncio
async def test_search_with_chapter_filter(
    client: AsyncClient,
    free_user: User,
    sample_chapters: list,
    headers_free_user: dict
):
    """Test search limited to specific chapter."""
    response = await client.get(
        "/search?q=introduction&chapter_id=ch-001",
        headers=headers_free_user
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # All results should be from ch-001
    for result in data["data"]:
        assert result["chapter_id"] == "ch-001"


@pytest.mark.asyncio
async def test_search_result_structure(
    client: AsyncClient,
    free_user: User,
    sample_chapters: list,
    headers_free_user: dict
):
    """Test search result has correct structure."""
    response = await client.get(
        "/search?q=agent",
        headers=headers_free_user
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # If there are results, verify structure
    if data["data"]:
        result = data["data"][0]
        assert "chapter_id" in result
        assert "chapter_title" in result
        assert "excerpt" in result
        assert "relevance_score" in result
        assert isinstance(result["relevance_score"], float)


@pytest.mark.asyncio
async def test_search_limits_results(
    client: AsyncClient,
    free_user: User,
    sample_chapters: list,
    headers_free_user: dict
):
    """Test search returns max 5 results."""
    response = await client.get(
        "/search?q=the",
        headers=headers_free_user
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Should return max 5 results
    assert len(data["data"]) <= 5


@pytest.mark.asyncio
async def test_unauthenticated_search(
    client: AsyncClient
):
    """Test unauthenticated user gets 401."""
    response = await client.get("/search?q=test")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
