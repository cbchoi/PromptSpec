from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from promptspec_api import AppSettings, SettingsRepository, create_app


def prompt_spec_payload() -> dict[str, object]:
    return {
        "id": "spec_001",
        "title": "API prompt",
        "parent_id": None,
        "slots": [
            {
                "key": "task",
                "type": "task",
                "value": "Summarize the design.",
                "condition": None,
                "priority": 100,
                "source": "user",
                "version": 1,
                "required": True,
            }
        ],
        "strategy": {
            "render_strategy": "plain",
            "validation_strategy": "strict",
            "inspection_strategy": "schema_bound",
        },
        "metadata": {},
    }


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def app_client(tmp_path: Path) -> AsyncClient:
    settings_repo = SettingsRepository(f"sqlite:///{tmp_path / 'settings.sqlite'}")
    app = create_app(settings_repo=settings_repo, root=Path("."))
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


@pytest.mark.anyio
async def test_prompt_resolve_render_validate(app_client: AsyncClient) -> None:
    resolve_response = await app_client.post("/api/prompts/resolve", json=prompt_spec_payload())
    assert resolve_response.status_code == 200

    render_response = await app_client.post("/api/prompts/render", json=resolve_response.json())
    assert render_response.status_code == 200
    rendered = render_response.json()
    assert rendered["text"] == "Summarize the design."

    validate_response = await app_client.post(
        "/api/prompts/validate",
        json={
            "prompt_spec": resolve_response.json(),
            "rendered_prompt": rendered,
            "meaning_report": None,
        },
    )
    assert validate_response.status_code == 200
    assert validate_response.json()["status"] == "pass"


@pytest.mark.anyio
async def test_inspect_endpoint_returns_meaning_report(app_client: AsyncClient) -> None:
    response = await app_client.post(
        "/api/prompts/inspect",
        json={"spec_id": "spec_001", "text": "Summarize.", "spans": []},
    )

    assert response.status_code == 200
    assert response.json()["meaning"] == {"text": "Summarize."}


@pytest.mark.anyio
async def test_settings_round_trip(app_client: AsyncClient) -> None:
    response = await app_client.put(
        "/api/settings",
        json=AppSettings(
            local_llm_endpoint="http://localhost:9999",
            storage_path=".promptspec/test.sqlite",
        ).model_dump(),
    )

    assert response.status_code == 200
    assert response.json()["local_llm_endpoint"] == "http://localhost:9999"

    get_response = await app_client.get("/api/settings")
    assert get_response.json()["storage_path"] == ".promptspec/test.sqlite"


@pytest.mark.anyio
async def test_tests_run_and_report_endpoint(app_client: AsyncClient) -> None:
    run_response = await app_client.post(
        "/api/tests/run",
        json={"suite": "scenario", "test_ids": []},
    )
    assert run_response.status_code == 200
    assert run_response.json()["status"] == "pass"

    report_response = await app_client.get("/api/tests/report/scenario_suite")
    assert report_response.status_code == 200
    assert report_response.json()["report_id"] == "scenario_suite"


@pytest.mark.anyio
async def test_ralph_status_and_check(app_client: AsyncClient) -> None:
    status_response = await app_client.get("/api/ralph/status")
    assert status_response.status_code == 200
    assert "tasks" in status_response.json()

    check_response = await app_client.post("/api/ralph/check", json={"task_id": "M1.T1"})
    assert check_response.status_code == 200
    assert check_response.json()["suite"] == "ralph"
