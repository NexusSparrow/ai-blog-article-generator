"""Local OpenAI-compatible server adapter (Ollama, LM Studio, llama.cpp server)."""
from __future__ import annotations

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter

from aiblog.config.settings import ProviderEndpoint
from aiblog.core.errors import ProviderError
from aiblog.core.interfaces import ArticleProvider


class LocalProvider(ArticleProvider):
    def __init__(self, endpoint: ProviderEndpoint, timeout_seconds: int, max_retries: int) -> None:
        self._endpoint = endpoint
        self._timeout = timeout_seconds
        self._max_retries = max_retries

    @property
    def name(self) -> str:
        return "local"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential_jitter(initial=0.5, max=6),
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
        }
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            resp = await client.post(
                f"{self._endpoint.base_url}/chat/completions",
                json=payload,
            )
        if resp.status_code >= 400:
            raise ProviderError(self.name, resp.status_code, resp.text[:400])
        data = resp.json()
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as exc:
            raise ProviderError(self.name, resp.status_code, "malformed response body") from exc