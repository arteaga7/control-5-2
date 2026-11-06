from pathlib import Path
import requests
import json
import os
from dotenv import load_dotenv
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_PATH)


def post_inbox(url=None):
    """Post API Rest to trigger PowerAutomate"""
    url = url or os.getenv("INBOX_URL")
    if not url:
        raise RuntimeError(f"No se encontró INBOX_URL en {ENV_PATH}")

    # json= pone el Content-Type solo
    response = requests.post(url, timeout=60, verify=False)

    if response.status_code in (200, 202):
        print("Exitoso")
    else:
        raise Exception(
            f"Power Automate fallo al checar la bandeja de entrada: "
            f"{response.status_code} - {response.text}"
        )


post_inbox()
