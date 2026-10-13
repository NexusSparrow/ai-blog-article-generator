"""OpenAI-compatible chat-completions adapter (also covers Azure/OpenRouter)."""
from __future__ import annotations

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter

import keyring

from aiblog.config.settings import ProviderEndpoint
from aiblog.core.errors import ProviderError
from aiblog.core.interfaces import ArticleProvider


class OpenAIProvider(ArticleProvider):
    def __init__(self, endpoint: ProviderEndpoint, timeout_seconds: int, max_retries: int) -> None:
        self._endpoint = endpoint
        self._timeout = timeout_seconds
        self._max_retries = max_retries

    @property
    def name(self) -> str:
        return "openai"

    def _api_key(self) -> str:
        key = keyring.get_password(self._endpoint.keyring_service, "api_key")
        if not key:
            raise ProviderError(self.name, None, "no API key in Windows Credential Manager")
        return key

    @retry(
        stop=stop_after_attempt(4),
        wait=wait_exponential_jitter(initial=1, max=20),
        retry=retry_if_exception_type(httpx.TransportError),
        reraise=True,
    )
    async def complete(self, system: str, prompt: str) -> str:
        payload = {
            "model": self._endpoint.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
        }
        headers = {"Authorization": f"Bearer {self._api_key()}"}
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            resp = await client.post(
                f"{self._endpoint.base_url}/chat/completions",
                json=payload,
                headers=headers,
            )
        if resp.status_code >= 400:
            raise ProviderError(self.name, resp.status_code, resp.text[:400])
        data = resp.json()
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as exc:
            raise ProviderError(self.name, resp.status_code, "malformed response body") from exc