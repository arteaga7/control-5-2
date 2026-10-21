"""
bot2.py: Check if there is evidence in the folder '1. CHI Report + Request' and
check if an email was sent to all the people responsible in the 'Responsable' column
of the CHI_Report
"""

from pathlib import Path
import argparse
from modules.chi_report import read_xlsm, compare_col_content
from modules.mail import read_msg, send_mail


PROJECT_DIR = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--month", default="03 March")
parser.add_argument("--unilever_path", type=Path, default=PROJECT_DIR)
args = parser.parse_args()
MONTH = "03 March"  # args.month
UNILEVER_PATH = Path(r"C:\SharePoints")  # args.unilever_path

FOLDER_PATH = (
    UNILEVER_PATH / "Unilever"
    / "Productivity Plan - Prueba Bot Controles delivery"
    / "Mexico" / "Deliver" / "OTB C5.2" / "2026"
)
COLS_CHI_REPORT = ["Responsable", "Approver", "Justificación"]
CHI_REPORT_FOLDER = Path(FOLDER_PATH) / MONTH / "1. CHI Report + Request"

body_missing_evidence = """Hola Equipo, 
 
Por favor subir las evidencias faltantes.

Saludos."""

body_mismatch_sent = """Hola Equipo, 
 
Por favor mandar un correo complementario a las personas que faltaron.

Saludos."""


def main():
    df = read_xlsm(CHI_REPORT_FOLDER, COLS_CHI_REPORT)
    mailto_chi_report = read_msg(folder_path=CHI_REPORT_FOLDER, n_mails=1,
                                 extension="*.msg", property="to")

    if df.empty or len(mailto_chi_report) == 0:
        print("No hay edivencia para evaluar,"
              "se mandara un correo a las personas correspondientes.")
        # send_mail(body_missing_evidence)
        return

    if len(mailto_chi_report) > 0:
        df = compare_col_content(df=df, col="Responsable",
                                 new_col="Enviado", mails=mailto_chi_report)

        if not df["Enviado"].all():
            df_filtered = df[(df["Enviado"] == False)]
            print(df_filtered[["Responsable", "Enviado"]], "\n")
            print("Faltaron personas al mandar el correo, "
                  "se mandara un correo a las personas correspondientes.")
            # send_mail(body_mismatch_sent)
            return
        print("Ejecución correcta, el correo se envio a todos los responsables.")


if __name__ == "__main__":
    main()
