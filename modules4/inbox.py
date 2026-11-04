# inbox.py

from pathlib import Path
import requests
import pandas as pd
from modules.mail import send_mail


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
    print(df[[col]])
    if inbox_evidence > 0:
        print("\nMandar correo para subir evidencia en SharePoint.")
    else:
        df_ans = df[df["Feedback"] == True]
        df_no_ans = df[df["Feedback"] == False]
        print("\nMandar correo para pedir subir evidencia para df_ans:\n", df_ans)
        print("\nMandar correo para escalar para df_no_ans:\n", df_no_ans)
    return []


def post_inbox():
    """Post API Rest to trgger PowerAutomate to obtain the emails"""
    sas = """https://defaultf66fae025d36495bbfe078a6ff9f8e.6e.environment.api.powerplatform.com:443/powerautomate/automations/direct/cu/10/workflows/dbcaa29207554d9da81374caf52b19ec/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=a8bqoi84j1nFwh1bUZ1_fTqQp-RW-FlBAVlAktm6c0M"""
    Headers = {"Content-Type": "application/json"}
    response = requests.post(sas, headers=Headers, verify=False)

    if response.status_code == 202:
        print("Exitoso")
    else:
        raise Exception(
            f"Power Automate fallo al checar la bandeja de entrada:  {response.status_code}")
