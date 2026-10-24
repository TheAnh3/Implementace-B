"""Simple in-memory storage for notes."""

from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class Note:
    id: str
    text: str


class NoteNotFoundError(LookupError):
    """Raised when an operation targets a note that does not exist."""


class NoteStore:
    """Store notes in process memory."""

    def __init__(self) -> None:
        self._notes: dict[str, Note] = {}

    def list_notes(self) -> list[Note]:
        return list(self._notes.values())

    def get_note(self, note_id: str) -> Note:
        try:
            return self._notes[note_id]
        except KeyError as exc:
            raise NoteNotFoundError(note_id) from exc

    def create_note(self, text: str) -> Note:
        note = Note(id=str(uuid4()), text=text)
        self._notes[note.id] = note
        return note

    def update_note(self, note_id: str, text: str) -> Note:
        if note_id not in self._notes:
            raise NoteNotFoundError(note_id)

        note = Note(id=note_id, text=text)
        self._notes[note_id] = note
        return note

    def delete_note(self, note_id: str) -> None:
        try:
            del self._notes[note_id]
        except KeyError as exc:
            raise NoteNotFoundError(note_id) from exc
