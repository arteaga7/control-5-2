# approval.py

from pathlib import Path
import pandas as pd
from modules.mail import send_mail
from modules.mail import read_msg, compare_col_content
from modules4.inbox import check_inbox


def approvals(df: pd.DataFrame, approvals_path: Path,
              col: str, new_col: str):
    """dd"""
    df_feedback = df[df["Feedback"] == True]
    print("\nSe procede a revisar aprobaciones de:")
    print(df_feedback[["Responsable", "Feedback"]])
    from_approver = read_msg(approvals_path,
                             extension="*.msg", property="sender")

    if len(from_approver) > 0:
        df_approver = compare_col_content(df_feedback, col,
                                          new_col, from_approver)
        print("df_approver:\n")
        print(df_approver)
        if not df_approver[new_col].all():
            pass
            # df_approver_filtered = df_approver[(df_approver[new_col] == False)]
            # print(df_approver_filtered[["Responsable", new_col]], "\n")
        else:
            print("Control Correcto")

    else:
        print("Verificar bandeja de entrada de todos los responsables (approvers).")
        check_inbox(df_feedback)
        return
