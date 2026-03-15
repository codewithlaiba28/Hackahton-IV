"""
LLM Service - Cerebras API Wrapper

This service provides LLM capabilities using Cerebras.

Constitutional Compliance:
- Principle VIII: Hybrid Selectivity Law (premium-only, user-initiated)
- Principle X: Cost Control Standards (logging, caps)
- Principle XI: LLM Quality Standards (grounding, structured output, fallbacks)
"""

import json
import time
import httpx
from typing import Tuple, Dict, Any, Optional
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.llm_usage import LLMUsage
from app.services.exceptions import LLMParseError, LLMUnavailableError


class LLMService:
    """
    Service for calling Cerebras API.
    
    Responsibilities:
    - Make async LLM calls
    - Parse JSON responses
    - Calculate costs
    - Log usage to database
    """
    
    # Cerebras pricing estimate (or set to 0 if free tier/fixed cost)
    # Llama 3.1 70B on Cerebras is very fast and often has specific pricing
    INPUT_TOKEN_COST = 0.000001
    OUTPUT_TOKEN_COST = 0.000001
    
    def __init__(self):
        """Initialize Cerebras configuration."""
        self.api_key = settings.CEREBRAS_API_KEY
        self.model = settings.CEREBRAS_MODEL
        self.base_url = "https://api.cerebras.ai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate LLM API cost."""
        input_cost = input_tokens * self.INPUT_TOKEN_COST
        output_cost = output_tokens * self.OUTPUT_TOKEN_COST
        return round(input_cost + output_cost, 6)
    
    async def call_claude(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
        feature_name: str,
        user_id: str,
        db: AsyncSession
    ) -> Tuple[Dict[str, Any], LLMUsage]:
        """
        Call Cerebras (maintaining interface name 'call_claude' for compatibility) and log usage.
        """
        start_time = time.time()
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": max_tokens,
            "response_format": {"type": "json_object"} if "JSON" in system_prompt else None
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    self.base_url,
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                
                # 2. Parse response text
                response_text = data["choices"][0]["message"]["content"]
                
                # 3. Parse JSON if expected
                try:
                    # Clean markdown if present
                    clean_text = response_text.strip()
                    if clean_text.startswith("```json"):
                        clean_text = clean_text[7:]
                    if clean_text.startswith("```"):
                        clean_text = clean_text[3:]
                    if clean_text.endswith("```"):
                        clean_text = clean_text[:-3]
                    clean_text = clean_text.strip()
                    
                    parsed_response = json.loads(clean_text)
                except json.JSONDecodeError as e:
                    # If not JSON, but we expect it, this might be an issue.
                    # But for simplicity, we'll try to return it as a dict if it was meant to be one.
                    raise LLMParseError(
                        f"Failed to parse LLM response as JSON: {str(e)}",
                        raw_response=response_text
                    )
                
                # 4. Calculate cost
                usage = data.get("usage", {})
                input_tokens = usage.get("prompt_tokens", 0)
                output_tokens = usage.get("completion_tokens", 0)
                total_cost = self._calculate_cost(input_tokens, output_tokens)
                
                # 5. Create LLMUsage record
                llm_usage = LLMUsage(
                    user_id=user_id,
                    feature_name=feature_name,
                    model=self.model,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    cost_usd=total_cost
                )
                
                # 6. Log to database
                db.add(llm_usage)
                await db.commit()
                await db.refresh(llm_usage)
                
                return (parsed_response, llm_usage)
                
            except httpx.TimeoutException:
                raise LLMUnavailableError("Cerebras API timed out")
            except httpx.HTTPStatusError as e:
                raise LLMUnavailableError(f"Cerebras API error: {e.response.status_code} - {e.response.text}")
            except Exception as e:
                raise LLMUnavailableError(f"Unexpected error calling Cerebras: {str(e)}")


# Global instance for dependency injection
llm_service = LLMService()
