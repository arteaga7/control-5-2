"""
bot4.py: Use folders "06 June", "07 July", ...
"""

from pathlib import Path
import argparse
from modules.chi_report import read_xlsm, compare_col_content
from modules.mail import read_msg, send_mail


PROJECT_DIR = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--month", default="06 June")
parser.add_argument("--unilever_path", type=Path, default=PROJECT_DIR)
args = parser.parse_args()
MONTH = "06 June"  # args.month
UNILEVER_PATH = Path(r"C:\SharePoints")  # args.unilever_path

FOLDER_PATH = (
    UNILEVER_PATH / "Unilever"
    / "Productivity Plan - Prueba Bot Controles delivery"
    / "Mexico" / "Deliver" / "OTB C5.2" / "2026"
)
COLS_CHI_REPORT = ["Responsable", "Approver", "Justificación"]
CHI_REPORT_FOLDER = Path(FOLDER_PATH) / MONTH / "1. CHI Report + Request"
JUSTIFICATION_FOLDER = Path(FOLDER_PATH) / MONTH / "2. Justifications"


body_ = """Hola Equipo, 
 
Por favor 

Saludos."""


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
        print("Verificar bandeja de entrada")

    print("Fin bot4.")


if __name__ == "__main__":
    main()
