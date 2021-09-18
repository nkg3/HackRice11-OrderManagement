import firebase_admin
from firebase_admin.credentials import Certificate
from firebase_admin import db
from pathlib import Path
from xlxs_parser import ExcelParser
debug: bool = False

"""
Call init_database first before anything!
"""


def init_database(url: str, cred_path: str):
    cred = Certificate(cred_path)
    default_app = firebase_admin.initialize_app(cred, {'databaseURL': url})


def set_with_dict(data: dict, dir_ref: str = "/"):
    reference = db.reference(dir_ref)
    reference.set(data)
    if debug:
        print("[Database set] source is dict, reference dir: " + dir_ref)


def set_with_excel(path: str, sheet_name: str, row_range: tuple, col_range: tuple, dir_ref: str = "/"):
    reference = db.reference(dir_ref)
    parser: ExcelParser = ExcelParser(Path(path))
    data = parser.parse_sheet(sheet_name, row_range, col_range)
    reference.set(data)
    if debug:
        print("[Database set] sheet name: " + sheet_name + ", reference dir: " + dir_ref)
