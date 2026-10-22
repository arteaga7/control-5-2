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

missing_report = """Hola Equipo,<br><br> 
 
Por favor subir el CHI Report.<br><br>

Saludos."""
missing_evidence = """Hola Equipo,<br><br>
 
Por favor subir la evidencia faltante.<br><br>

Saludos."""

mismatch_sent_template = """Hola Equipo,<br><br>
 
Por favor mandar un correo complementario a las personas que faltaron:<br><br>
{df}
<br><br>
Saludos."""

bot2_success = """Hola Equipo,<br><br>
 
La evidencia se recibio con exito.<br><br>

Saludos."""


def notify(mensaje_log: str, correo_html: str):
    """Imprime un mensaje de log y envía el correo correspondiente."""
    print(mensaje_log)
    send_mail(correo_html)


def main():
    df = read_xlsm(CHI_REPORT_FOLDER, COLS_CHI_REPORT)
    if df.empty:
        notify(
            "No hay CHI_Report.\nSe envia el sig. correo...\n"+missing_report, missing_report)
        return

    mailto_chi_report = read_msg(folder_path=CHI_REPORT_FOLDER, n_mails=1,
                                 extension="*.msg", property="to")

    if len(mailto_chi_report) == 0:
        notify("No hay correo de evidencia para evaluar.\nSe envia el sig. correo...\n"
               + missing_evidence, missing_evidence)
        return

    if len(mailto_chi_report) > 0:
        df = compare_col_content(df=df, col="Responsable",
                                 new_col="Enviado", mails=mailto_chi_report)
        print("Personas responsables:")
        print(df[["Responsable", "Enviado"]], "\n")

        if not df["Enviado"].all():
            df_not_sent = df[(df["Enviado"] == False)]
            df_not_sent = df_not_sent[["Responsable", "Enviado"]]
            mismatch_sent = mismatch_sent_template.format(
                df=df_not_sent.to_html(index=False))
            mismatch_sent_pandas = mismatch_sent_template.format(
                df=df_not_sent.to_string(index=False))
            print(
                "\nSe envia el sig. correo...\n", mismatch_sent_pandas)
            send_mail(mismatch_sent)
            return

        print("Ejecución correcta, el correo se envio a todos los responsables.")
        send_mail(bot2_success)


if __name__ == "__main__":
    main()
