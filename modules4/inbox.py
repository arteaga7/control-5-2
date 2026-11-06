# inbox.py

from pathlib import Path
import requests
import json
import os
from dotenv import load_dotenv
import pandas as pd

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_PATH)


def check_inbox(df: pd.DataFrame, col: str, working_dir: Path) -> list[str]:
    """The received DataFrame has column "Responsable"."""
    inbox_evidence = 0
    if col == "Responsable":
        folder_path = working_dir / "2. Justifications"
    elif col == "Approver":
        folder_path = working_dir / "3. Approvals"
    else:
        folder_path = working_dir / "2. Justifications"
    print(
        f"\nSe debe verificar la bandeja de entrada, en el folder {folder_path} para:")
    print(df[[col]].to_dict())
    return []


def post_inbox(df: pd.DataFrame, url=None):
    """Post API Rest to trigger PowerAutomate and send a DataFrame"""
    print("Aqui vamos\n")
    url = url or os.getenv("PA_INBOX_URL")
    if not url:
        raise RuntimeError(f"No se encontró PA_INBOX_URL en {ENV_PATH}")

    # to_json maneja NaN -> null y fechas -> ISO; json.loads lo vuelve lista de dicts
    registros = json.loads(df.to_json(orient="records", date_format="iso"))
    print(registros)
    payload = {
        "data": registros
    }

    # json= pone el Content-Type solo
    response = requests.post(url, json=payload, timeout=60, verify=False)

    if response.status_code in (200, 202):
        print("Exitoso")
    else:
        raise Exception(
            f"Power Automate fallo al checar la bandeja de entrada: "
            f"{response.status_code} - {response.text}"
        )
