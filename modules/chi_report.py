# chi_report.py:
from pathlib import Path
import pandas as pd


def get_filenames(folder_path: Path, extension: str) -> list[str]:
    """Regresa los nombres de todos los archivos que coincidan
    con la extensión."""
    return [file.name for file in folder_path.glob(extension) if file.is_file()]


def read_chi_report(file_path: str | Path, cols: list[str]) -> pd.DataFrame:
    """Lee el archivo '.xlsm' en la hoja 'Reporte' y extrae las columnas
    "Responsable", "Approver" y "Justificación"."""
    if not file_path.is_file():
        raise FileNotFoundError(
            f"No se encontró el CHI Report: {file_path}"
        )
    try:
        df = pd.read_excel(
            file_path,
            sheet_name="Reporte",
            usecols=cols,
            engine="openpyxl"
        )
    except ValueError as error:
        raise ValueError(
            "No se encontro la hoja o las columnas esperadas. "
            f"Columnas requeridas: {cols}"
        ) from error
    return df


def read_xlsm(folder_path: Path, cols: list[str]) -> pd.DataFrame:
    """Read the firts xlsm file, it should be only one."""
    xlsm_name = get_filenames(folder_path, extension="*.xlsm")
    if len(xlsm_name) > 0:
        xlsm_name = xlsm_name[0]
    else:
        print(f"No se encontró ningún archivo .xlsm en {folder_path}")
        return pd.DataFrame()

    return read_chi_report(
        file_path=folder_path / xlsm_name,
        cols=cols
    )


def compare_col_content(df: pd.DataFrame, col: str, new_col: str,
                        mails: list[str]) -> pd.DataFrame:
    """Compare content in column "col" with "mails and create a new column"""
    df = df.copy()
    df[new_col] = df[col].isin(mails)
    return df


def save_excel(df: pd.DataFrame, output_file: str, hoja: str = "Hoja1"):
    """Save dataframe in an Excel file"""
    with pd.ExcelWriter(output_file, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, sheet_name=hoja, index=False)
    print(f"Dataframe guardado: {output_file}")
    return
