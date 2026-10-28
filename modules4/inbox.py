# inbox.py

from pathlib import Path
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
