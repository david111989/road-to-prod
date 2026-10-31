from contextlib import asynccontextmanager

import psycopg
from fastapi import FastAPI
from pydantic import BaseModel

from app.config import get_settings


def get_conn():
    return psycopg.connect(get_settings().database_url)


@asynccontextmanager
async def lifespan(app: FastAPI):
    with get_conn() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS entries ("
            "id SERIAL PRIMARY KEY, "
            "name TEXT NOT NULL, "
            "message TEXT NOT NULL, "
            "created_at TIMESTAMPTZ NOT NULL DEFAULT now())"
        )
    yield


app = FastAPI(title="Guestbook", lifespan=lifespan)


class EntryIn(BaseModel):
    name: str
    message: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/entries")
def list_entries():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, name, message, created_at FROM entries "
            "ORDER BY id DESC LIMIT 50"
        ).fetchall()
    return [
        {"id": r[0], "name": r[1], "message": r[2], "created_at": r[3]}
        for r in rows
    ]


@app.post("/entries", status_code=201)
def add_entry(entry: EntryIn):
    with get_conn() as conn:
        row = conn.execute(
            "INSERT INTO entries (name, message) VALUES (%s, %s) RETURNING id",
            (entry.name, entry.message),
        ).fetchone()
    return {"id": row[0]}
