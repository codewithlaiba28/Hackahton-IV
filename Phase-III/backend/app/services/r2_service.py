# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.

from functools import lru_cache
from pathlib import Path
from typing import Optional
import time

from app.config import get_settings

settings = get_settings()


class ContentNotFoundError(Exception):
    """Raised when content is not found in storage."""
    pass


class LocalStorageService:
    """Local filesystem storage service for content.

    100% free alternative to Cloudflare R2 for Phase 1.
    Stores content in local files instead of cloud storage.
    """

    def __init__(self):
        """Initialize local storage client."""
        self.content_path = Path(settings.LOCAL_CONTENT_PATH)
        self.content_path.mkdir(parents=True, exist_ok=True)

        # Simple in-memory cache
        self._cache = {}
        self._cache_timestamps = {}
        self._cache_ttl = 300  # 5 minutes

    def get_chapter_content(self, chapter_id: str) -> str:
        """Get chapter content from local filesystem.

        Args:
            chapter_id: Chapter ID (e.g., 'ch-001')

        Returns:
            str: Raw Markdown content from file

        Raises:
            ContentNotFoundError: If content doesn't exist
        """
        cache_key = f"chapter:{chapter_id}"

        # Check cache first
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]

        # Read from local file
        content_file = self.content_path / "chapters" / chapter_id / "content.md"

        if not content_file.exists():
            raise ContentNotFoundError(f"Chapter {chapter_id} not found")

        content = content_file.read_text(encoding='utf-8')

        # Cache the content
        self._cache[cache_key] = content
        self._cache_timestamps[cache_key] = time.time()

        return content

    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached content is still valid."""
        if cache_key not in self._cache:
            return False

        age = time.time() - self._cache_timestamps.get(cache_key, 0)
        return age < self._cache_ttl


class R2Service:
    """Cloudflare R2 service for content storage.

    Implements simple LRU cache to reduce R2 API calls.
    Note: Requires boto3 and R2 credentials. Not used in free setup.
    """

    def __init__(self):
        """Initialize R2 client."""
        import boto3
        from botocore.config import Config
        
        self.client = boto3.client(
            's3',
            endpoint_url=settings.R2_ENDPOINT_URL,
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            config=Config(signature_version='s3v4'),
        )
        self.bucket_name = settings.R2_BUCKET_NAME

        # Simple in-memory cache (production should use Redis)
        self._cache = {}
        self._cache_timestamps = {}
        self._cache_ttl = 300  # 5 minutes

    def get_chapter_content(self, chapter_id: str) -> str:
        """Get chapter content from R2."""
        cache_key = f"chapter:{chapter_id}"

        # Check cache first
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]

        # Fetch from R2
        content_key = f"chapters/{chapter_id}/content.md"

        try:
            response = self.client.get_object(
                Bucket=self.bucket_name,
                Key=content_key
            )
            content = response['Body'].read().decode('utf-8')

            # Cache the content
            self._cache[cache_key] = content
            self._cache_timestamps[cache_key] = time.time()

            return content

        except self.client.exceptions.NoSuchKey:
            raise ContentNotFoundError(f"Chapter {chapter_id} not found in R2")

    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached content is still valid."""
        if cache_key not in self._cache:
            return False

        age = time.time() - self._cache_timestamps.get(cache_key, 0)
        return age < self._cache_ttl


# Factory function to get appropriate service based on config
@lru_cache()
def get_storage_service():
    """Get storage service instance (Local or R2 based on config)."""
    if settings.STORAGE_TYPE == "local":
        return LocalStorageService()
    else:
        return R2Service()


# Backward compatibility alias
def get_r2_service():
    """Get storage service (alias for get_storage_service)."""
    return get_storage_service()
