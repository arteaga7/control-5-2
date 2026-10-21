# inbox.py

import pandas as pd
from modules.mail import send_mail


def check_inbox(df_no_feedback: pd.DataFrame) -> list[str]:
    """The received DataFrame has column "Responsable"."""
    print("\nSe debe verificar la bandeja de entrada para:")
    print(df_no_feedback[["Responsable", "Feedback"]])
    return []
