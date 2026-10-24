"""Unit tests for the in-memory note store."""

import pytest

from app.store import NoteNotFoundError, NoteStore


def test_create_and_get_note() -> None:
    store = NoteStore()

    created = store.create_note("A note")

    assert created.id
    assert store.get_note(created.id) == created


def test_created_notes_have_unique_ids() -> None:
    store = NoteStore()

    first = store.create_note("First")
    second = store.create_note("Second")

    assert first.id != second.id


def test_list_notes_returns_all_notes() -> None:
    store = NoteStore()
    first = store.create_note("First")
    second = store.create_note("Second")

    assert store.list_notes() == [first, second]


def test_update_note_replaces_text_and_preserves_id() -> None:
    store = NoteStore()
    original = store.create_note("Before")

    updated = store.update_note(original.id, "After")

    assert updated.id == original.id
    assert updated.text == "After"
    assert store.get_note(original.id) == updated


def test_delete_note_removes_it() -> None:
    store = NoteStore()
    note = store.create_note("To delete")

    store.delete_note(note.id)

    assert store.list_notes() == []
    with pytest.raises(NoteNotFoundError):
        store.get_note(note.id)


@pytest.mark.parametrize("operation", ["get", "update", "delete"])
def test_operations_on_unknown_note_raise_error(operation: str) -> None:
    store = NoteStore()

    with pytest.raises(NoteNotFoundError):
        if operation == "get":
            store.get_note("missing")
        elif operation == "update":
            store.update_note("missing", "Updated")
        else:
            store.delete_note("missing")
