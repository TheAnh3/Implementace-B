"""Integration tests for the HTTP API."""

from fastapi.testclient import TestClient

from app.main import create_app
from app.store import NoteStore


def make_client() -> TestClient:
    return TestClient(create_app(NoteStore()))


def test_health_returns_json_status() -> None:
    response = make_client().get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_notes_can_be_created_listed_and_retrieved() -> None:
    client = make_client()

    created = client.post("/notes", json={"text": "  Buy milk  "})
    assert created.status_code == 201
    note = created.json()
    assert note["text"] == "Buy milk"
    assert note["id"]

    assert client.get("/notes").json() == [note]
    assert client.get(f"/notes/{note['id']}").json() == note


def test_note_can_be_updated_and_deleted() -> None:
    client = make_client()
    note = client.post("/notes", json={"text": "Before"}).json()

    updated = client.put(f"/notes/{note['id']}", json={"text": "After"})
    assert updated.status_code == 200
    assert updated.json() == {"id": note["id"], "text": "After"}

    deleted = client.delete(f"/notes/{note['id']}")
    assert deleted.status_code == 200
    assert deleted.json() == {"deleted": True, "id": note["id"]}
    assert client.get(f"/notes/{note['id']}").status_code == 404


def test_empty_or_missing_text_returns_validation_error() -> None:
    client = make_client()

    for payload in ({"text": "   "}, {}, {"text": 12}):
        response = client.post("/notes", json=payload)
        assert response.status_code == 422
        assert response.json()["error"]["code"] == "validation_error"


def test_update_requires_valid_text() -> None:
    client = make_client()
    note = client.post("/notes", json={"text": "Original"}).json()

    response = client.put(f"/notes/{note['id']}", json={"text": "  "})

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"
    assert client.get(f"/notes/{note['id']}").json()["text"] == "Original"


def test_missing_note_and_unknown_endpoint_have_distinct_errors() -> None:
    client = make_client()

    missing_note = client.get("/notes/does-not-exist")
    missing_endpoint = client.get("/unknown")

    assert missing_note.status_code == missing_endpoint.status_code == 404
    assert missing_note.json()["error"]["code"] == "note_not_found"
    assert missing_endpoint.json()["error"]["code"] == "endpoint_not_found"


def test_update_and_delete_missing_note_return_not_found() -> None:
    client = make_client()

    update = client.put("/notes/missing", json={"text": "Text"})
    delete = client.delete("/notes/missing")

    assert update.status_code == delete.status_code == 404
    assert update.json()["error"]["code"] == "note_not_found"
    assert delete.json()["error"]["code"] == "note_not_found"


def test_all_notes_are_lost_when_a_new_app_is_created() -> None:
    first_client = make_client()
    first_client.post("/notes", json={"text": "Temporary"})

    second_client = make_client()

    assert second_client.get("/notes").json() == []
