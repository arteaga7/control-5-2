"""
bot4.py: 4
"""

from pathlib import Path
import argparse
from modules.chi_report import read_xlsm, compare_col_content, save_excel
from modules.mail import read_msg, send_mail


PROJECT_DIR = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--month", default="03 March")
parser.add_argument("--unilever_path", type=Path, default=PROJECT_DIR)
args = parser.parse_args()
MONTH = "02 February"  # args.month
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
    mailto_chi_report = read_msg(folder_path=CHI_REPORT_FOLDER, n_mails=1,
                                 extension="*.msg", property="to")

    if df.empty or len(mailto_chi_report) == 0:
        print("No hay edivencia para evaluar.")
        # send_mail(body_missing_evidence)
        return

    df = compare_col_content(df=df, col="Responsable",
                             new_col="Enviado", mails=mailto_chi_report)

    print("Fin bot4.")


if __name__ == "__main__":
    main()
