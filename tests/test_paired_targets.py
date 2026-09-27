from relmote.agent_profiles import save_profile
from relmote.paired_targets import PairedTargetService


class FakeClient:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token
        self.calls = []

    def session(self):
        self.calls.append(("session",))
        return {"state": "active", "session_id": "session-1"}

    def info(self):
        self.calls.append(("info",))
        return {
            "role": "target",
            "target": {"name": "target-a-node"},
            "platform": {"system": "linux", "architecture": "x86_64"},
            "relmote": {
                "display_version": "0.1.0-dev.12",
                "commit": "abcdef1234567890",
                "short_commit": "abcdef12",
                "channel": "repository",
            },
            "session": {"state": "active", "workspace": "/workspace"},
        }

    def list(self, path="."):
        self.calls.append(("list", path))
        return [{"name": "README.md", "type": "file"}]

    def read(self, path):
        self.calls.append(("read", path))
        return "hello\n"

    def exec(self, argv, *, cwd=".", timeout=30):
        self.calls.append(("exec", argv, cwd, timeout))
        return {"stdout": "ok\n", "stderr": "", "returncode": 0}


def save_test_profile():
    return save_profile(
        name="target-a",
        base_url="https://target-a.example.invalid",
        token="secret-bearer",
        session={
            "workspace": "/workspace",
            "state": "active",
            "capabilities": ["workspace.list", "workspace.read", "terminal.exec"],
        },
    )


def test_targets_returns_credential_blind_profile_summaries(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    save_test_profile()

    service = PairedTargetService()
    targets = service.targets()

    assert targets == [
        {
            "name": "target-a",
            "workspace": "/workspace",
            "state": "active",
            "capabilities": [
                "workspace.list",
                "workspace.read",
                "terminal.exec",
            ],
        }
    ]
    assert "token" not in targets[0]
    assert "base_url" not in targets[0]


def test_service_reuses_profile_credentials_without_returning_them(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    save_test_profile()
    clients = []

    def client_factory(base_url, token):
        client = FakeClient(base_url, token)
        clients.append(client)
        return client

    service = PairedTargetService(client_factory=client_factory)

    assert service.status("target-a")["state"] == "active"
    assert service.info("target-a")["target"]["name"] == "target-a-node"
    assert service.list("target-a", "src")[0]["name"] == "README.md"
    assert service.read("target-a", "README.md") == "hello\n"
    assert service.exec(
        "target-a",
        ["git", "status"],
        cwd="repo",
        timeout=12,
    )["returncode"] == 0

    assert all(client.base_url == "https://target-a.example.invalid" for client in clients)
    assert all(client.token == "secret-bearer" for client in clients)
    assert clients[0].calls == [("session",)]
    assert clients[1].calls == [("info",)]
    assert clients[2].calls == [("list", "src")]
    assert clients[3].calls == [("read", "README.md")]
    assert clients[4].calls == [("exec", ["git", "status"], "repo", 12)]


def test_targets_marks_unreadable_profiles_without_exposing_file_contents(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    path = tmp_path / "relmote" / "agents"
    path.mkdir(parents=True)
    (path / "broken.json").write_text("{not-json")

    service = PairedTargetService()

    assert service.targets() == [
        {
            "name": "broken",
            "workspace": None,
            "state": "unreadable",
            "capabilities": [],
        }
    ]
