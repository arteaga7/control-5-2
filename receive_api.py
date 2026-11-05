import base64
import json
import os
import re
import secrets
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Union
from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

#uvicorn receive_api:app --host 0.0.0.0 --port 8000
#http://localhost:8000/docs
# --- Configuración ---
API_KEY = os.getenv("INBOX_API_KEY", "mi-clave-secreta")
DATA_DIR = Path(os.getenv("INBOX_DATA_DIR", "data/emails"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Inbox Receiver API")


# --- Modelos ---
class Attachment(BaseModel):
    model_config = ConfigDict(extra="allow")
    name: str
    contentBytes: Optional[str] = None   # base64, como lo manda Power Automate
    contentType: Optional[str] = None


class Email(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: Optional[str] = None
    subject: Optional[str] = None
    sender: Optional[str] = Field(None, alias="from")
    to: Optional[str] = None
    cc: Optional[str] = None
    receivedDateTime: Optional[str] = None
    body: Optional[str] = None
    attachments: List[Attachment] = []


# --- Helpers ---
def check_key(x_api_key: Optional[str]) -> None:
    if not x_api_key or not secrets.compare_digest(x_api_key, API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="API key inválida")


def safe_name(text: str) -> str:
    return re.sub(r'[<>:"/\\|?*\s]+', "_", text).strip("_")[:80] or "sin_nombre"


def save_email(email: Email) -> str:
    # Decodificar primero, para no crear carpetas si algo viene mal
    decoded = []
    for att in email.attachments:
        if att.contentBytes:
            try:
                decoded.append((att.name, base64.b64decode(
                    att.contentBytes, validate=True)))
            except (ValueError, base64.binascii.Error):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El adjunto '{att.name}' no tiene contentBytes en base64 válido",
                )

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    folder = DATA_DIR / f"{stamp}_{safe_name(email.subject or 'sin_asunto')}"
    folder.mkdir(parents=True, exist_ok=True)

    saved = []
    for name, content in decoded:
        (folder / safe_name(name)).write_bytes(content)
        saved.append(name)

    meta = email.model_dump(by_alias=True, exclude={"attachments"})
    meta["attachments_saved"] = saved
    (folder / "email.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return folder.name


# --- Endpoints ---
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/emails", status_code=status.HTTP_201_CREATED)
def receive_emails(
    payload: Union[List[Email], Email],
    x_api_key: Optional[str] = Header(None),
):
    check_key(x_api_key)
    emails = payload if isinstance(payload, list) else [payload]
    saved = [save_email(e) for e in emails]
    return {"received": len(saved), "saved": saved}


@app.get("/emails")
def list_emails(x_api_key: Optional[str] = Header(None)):
    check_key(x_api_key)
    return sorted([p.name for p in DATA_DIR.iterdir() if p.is_dir()], reverse=True)
