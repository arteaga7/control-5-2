"""
bot4.py: Use folders "06 June", "07 July", ...
"""

from pathlib import Path
import argparse
from modules.chi_report import read_xlsm, compare_col_content
from modules.mail import read_msg, send_mail, print_mail
from modules4.inbox import extraer_from_carpeta

PROJECT_DIR = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--month", default="09 September")
parser.add_argument("--unilever_path", type=Path, default=PROJECT_DIR)
args = parser.parse_args()
MONTH = "09 September"  # args.month
UNILEVER_PATH = Path(r"C:\SharePoints")  # args.unilever_path
CAPGEMINI_FOLDER_PATH = UNILEVER_PATH / "Unilever" / "SKY_CE - emails_capgemini"

FOLDER_PATH = (
    UNILEVER_PATH / "Unilever"
    / "Productivity Plan - Prueba Bot Controles delivery"
    / "Mexico" / "Deliver" / "OTB C5.2" / "2026"
)
COLS_CHI_REPORT = ["Responsable", "Approver", "Justificación"]
CHI_REPORT_FOLDER = Path(FOLDER_PATH) / MONTH / "1. CHI Report + Request"
JUSTIFICATION_FOLDER = Path(FOLDER_PATH) / MONTH / "2. Justifications"
APPOVAL_FOLDER = Path(FOLDER_PATH) / MONTH / "3. Approvals"
WORKING_DIR = Path(FOLDER_PATH) / MONTH
# --------Mail content ------------
success_template = """Hola Equipo,<br><br>
Control 5.2 correcto para:<br><br>
{df}
<br><br>
Saludos."""
# ----------------------------------


def main():
    df = read_xlsm(CHI_REPORT_FOLDER, COLS_CHI_REPORT)
    if df.empty:
        print("No hay CHI_Report. Ejecute bot2 para mandar correo correspondiente" +
              "o si hizo modificaciones recientemente, espere unos minutos y vuelva a intentar.")
        return
    from_justifications = read_msg(folder_path=JUSTIFICATION_FOLDER,
                                   extension="*.msg", property="sender")

    if len(from_justifications) > 0:
        df = compare_col_content(df=df, col="Responsable",
                                 new_col="Feedback", mails=from_justifications)
        print("Personas que respondieron (mandaron mail de justificacion):")
        print(df[["Responsable", "Feedback"]], "\n")

    else:
        print("Verificar bandeja de entrada para justificaciones.")
        # post_inbox()
        # check_inbox_sharepoint("Responsable", WORKING_DIR)
        return

    # df_feed = df[df["Feedback"] == True]
    df_no_feed = df[df["Feedback"] == False]

    if not df_no_feed.empty:
        # post_inbox()
        remitentes = extraer_from_carpeta(CAPGEMINI_FOLDER_PATH)
        print(remitentes)

    """
    from_approver = read_msg(folder_path=APPOVAL_FOLDER,
                             extension="*.msg", property="sender")
    if len(from_approver) > 0:
        df_feed = compare_col_content(df=df_feed, col="Approver",
                                      new_col="Aprobacion", mails=from_approver)
        df_aprove = df_feed[df_feed["Aprobacion"] == True]
        df_no_aprove = df_feed[df_feed["Aprobacion"] == False]

        if not df_no_aprove.empty:
            post_inbox()
            # check_inbox(df_no_aprove, "Approver", WORKING_DIR)
        if not df_aprove.empty:
            df_success = df_aprove[["Responsable", "Approver", "Aprobacion"]]
            # print_mail("Control correcto para:", df_success, success_template)

    else:
        print("Verificar bandeja de entrada de todos los aprovadores.")
        post_inbox()
        # check_inbox(df_feed, "Approver", WORKING_DIR)
        return
    """


if __name__ == "__main__":
    main()
