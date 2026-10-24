"""FastAPI application exposing CRUD operations for notes."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.models import NoteInput, NoteResponse
from app.store import NoteNotFoundError, NoteStore


def create_app(store: NoteStore | None = None) -> FastAPI:
    """Create the API application, optionally with an injected note store."""

    note_store = store or NoteStore()
    api = FastAPI(title="Notes API", version="1.0.0")

    @api.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        details = [
            {
                "field": ".".join(str(part) for part in error["loc"]),
                "message": error["msg"],
            }
            for error in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "validation_error",
                    "message": "Request validation failed.",
                    "details": details,
                }
            },
        )

    @api.exception_handler(NoteNotFoundError)
    async def note_not_found_handler(
        request: Request, exc: NoteNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={
                "error": {
                    "code": "note_not_found",
                    "message": "Note not found.",
                }
            },
        )

    @api.exception_handler(StarletteHTTPException)
    async def http_error_handler(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        if exc.status_code == 404:
            code = "endpoint_not_found"
            message = "Endpoint not found."
        elif exc.status_code == 405:
            code = "method_not_allowed"
            message = "Method not allowed."
        else:
            code = "http_error"
            message = str(exc.detail)

        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": code, "message": message}},
            headers=exc.headers,
        )

    @api.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @api.get("/notes", response_model=list[NoteResponse])
    def list_notes() -> list[NoteResponse]:
        return [
            NoteResponse(id=note.id, text=note.text)
            for note in note_store.list_notes()
        ]

    @api.get("/notes/{note_id}", response_model=NoteResponse)
    def get_note(note_id: str) -> NoteResponse:
        note = note_store.get_note(note_id)
        return NoteResponse(id=note.id, text=note.text)

    @api.post("/notes", response_model=NoteResponse, status_code=201)
    def create_note(payload: NoteInput) -> NoteResponse:
        note = note_store.create_note(payload.text)
        return NoteResponse(id=note.id, text=note.text)

    @api.put("/notes/{note_id}", response_model=NoteResponse)
    def update_note(note_id: str, payload: NoteInput) -> NoteResponse:
        note = note_store.update_note(note_id, payload.text)
        return NoteResponse(id=note.id, text=note.text)

    @api.delete("/notes/{note_id}")
    def delete_note(note_id: str) -> dict[str, str | bool]:
        note_store.delete_note(note_id)
        return {"deleted": True, "id": note_id}

    return api


app = create_app()
