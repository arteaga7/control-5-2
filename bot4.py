"""
bot4.py: Use folders "06 June", "07 July", ...
"""

from pathlib import Path
import argparse
from modules.chi_report import read_xlsm, compare_col_content
from modules.mail import read_msg
from modules4.inbox import check_inbox
from modules4.approval import approvals

PROJECT_DIR = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--month", default="06 June")
parser.add_argument("--unilever_path", type=Path, default=PROJECT_DIR)
args = parser.parse_args()
MONTH = "07 July"  # args.month
UNILEVER_PATH = Path(r"C:\SharePoints")  # args.unilever_path

FOLDER_PATH = (
    UNILEVER_PATH / "Unilever"
    / "Productivity Plan - Prueba Bot Controles delivery"
    / "Mexico" / "Deliver" / "OTB C5.2" / "2026"
)
COLS_CHI_REPORT = ["Responsable", "Approver", "Justificación"]
CHI_REPORT_FOLDER = Path(FOLDER_PATH) / MONTH / "1. CHI Report + Request"
JUSTIFICATION_FOLDER = Path(FOLDER_PATH) / MONTH / "2. Justifications"
APPOVAL_FOLDER = Path(FOLDER_PATH) / MONTH / "3. Approvals"


def main():
    df = read_xlsm(CHI_REPORT_FOLDER, COLS_CHI_REPORT)
    if df.empty:
        print("No hay CHI_Report.")
        return

    from_justifications = read_msg(folder_path=JUSTIFICATION_FOLDER,
                                   extension="*.msg", property="sender")

    if len(from_justifications) > 0:
        df = compare_col_content(df=df, col="Responsable",
                                 new_col="Feedback", mails=from_justifications)

    else:
        print("Verificar bandeja de entrada de todos los responsables.")
        check_inbox(df)
        return

    print("Personas que respondieron (mandaron mail de justificacion):")
    print(df[["Responsable", "Feedback"]], "\n")
    approvals(df, APPOVAL_FOLDER, "Approver", "Aprobacion")

    df_no_feedback = df[df["Feedback"] == False]
    if not df_no_feedback.empty:
        check_inbox(df_no_feedback)


if __name__ == "__main__":
    main()
