from __future__ import annotations

import json
import urllib.error
import urllib.request


class RelmoteAgentClient:
    def __init__(
        self,
        base_url: str,
        token: str,
        *,
        timeout: int = 15,
    ):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout

    def _request(self, path: str, payload: dict | None = None) -> dict:
        data = None if payload is None else json.dumps(payload).encode()
        request = urllib.request.Request(
            self.base_url + path,
            data=data,
            method="GET" if payload is None else "POST",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read())
        except urllib.error.HTTPError as exc:
            try:
                detail = json.loads(exc.read()).get("error", exc.reason)
            except Exception:
                detail = exc.reason
            raise PermissionError(f"Relmote Agent API: {detail}") from exc

    def session(self) -> dict:
        return self._request("/api/v1/agent/session")

    def list(self, path: str = ".") -> list[dict]:
        return self._request("/api/v1/agent/list", {"path": path})["entries"]

    def read(self, path: str) -> str:
        return self._request("/api/v1/agent/read", {"path": path})["text"]

    def exec(
        self,
        argv: list[str],
        *,
        cwd: str = ".",
        timeout: int = 30,
    ) -> dict:
        return self._request(
            "/api/v1/agent/exec",
            {"argv": argv, "cwd": cwd, "timeout": timeout},
        )
