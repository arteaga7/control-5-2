# approval.py
import pandas as pd
from modules.mail import send_mail


def approvals(df_feedback: pd.DataFrame):
    """dd"""
    print("\nSe procede a revisar aprobaciones de:")
    print(df_feedback[["Responsable", "Feedback"]])
