# create_folders.py: Functions related to 'create_folder_structure' function in bot1.py
from pathlib import Path


def create_folder_structure(base_path, folders, subfolders):
    """Crea cada folder y, dentro de cada uno, los subfolders indicados."""
    base_path = Path(base_path)
    for folder in folders:
        for subfolder in subfolders:
            path = base_path / folder / subfolder
            path.mkdir(parents=True, exist_ok=True)
    print("Carpetas faltantes creadas!")
