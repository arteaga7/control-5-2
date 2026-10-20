# bot1.py: All folders are created
from pathlib import Path
import argparse
from modules.create_folders import create_folder_structure

PROJECT_DIR = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--unilever_path", type=Path, default=PROJECT_DIR)
args = parser.parse_args()
UNILEVER_PATH = args.unilever_path

FOLDER_PATH = (
    UNILEVER_PATH / "Unilever"
    / "Productivity Plan - Prueba Bot Controles delivery"
    / "Mexico" / "Deliver" / "OTB C5.2" / "2026"
)

folders = ["01 January", "02 February", "03 March", "04 April", "05 May", "06 June",
           "07 July", "08 August", "09 September", "10 October", "11 November",
           "12 Dicember"]
subfolders = ["1. CHI Report + Request", "2. Justifications", "3. Approvals"]


if __name__ == "__main__":
    create_folder_structure(FOLDER_PATH, folders, subfolders)
