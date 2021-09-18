import firebase_admin
from firebase_admin.credentials import Certificate
from firebase_admin import db
from pathlib import Path
from xlxs_parser import ExcelParser
DEBUG: bool = False
PRINT_DATA: bool = True


"""
Call init_database first before anything!
"""


def init_database(url: str, cred_path: str):
    cred = Certificate(cred_path)
    default_app = firebase_admin.initialize_app(cred, {'databaseURL': url})


def set_with_dict(data: dict, dir_ref: str = "/"):
    reference = db.reference(dir_ref)
    reference.set(data)
    if DEBUG:
        print("[Database set] source is dict, reference dir: " + dir_ref)
    if PRINT_DATA:
        print(data)


def set_with_excel(path: str, sheet_name: str, row_range: tuple, col_range: tuple, dir_ref: str = "/"):
    reference = db.reference(dir_ref)
    parser: ExcelParser = ExcelParser(Path(path))
    data = parser.parse_sheet(sheet_name, row_range, col_range)
    reference.set(data)
    if DEBUG:
        print("[Database set] sheet name: " + sheet_name + ", reference dir: " + dir_ref)
    if PRINT_DATA:
        print(data)


def get_under_directory(dir_ref: str, child_key: str = "", child_value: str = "") -> object:
    """
    get values from database
    Functionalities:
        get a dictionary of all children under the directory (THIS DEFINITELY WORKS RIGHT NOW)
        get one child given the child_key and child_value (specify child_key and child_value)
        get an OrderedDict of children given a key to index with (specify indexing_key)
    :param dir_ref: directory of the data
    :param child_key: key of child to index with
    :param child_value: value of child
    :return: A dict if only given dir_ref. An OrderedDict if given other parameters
    """
    reference = db.reference(dir_ref)
    if not child_value == "":
        return reference.order_by_child(child_key).equal_to(child_value).get()
    if (not child_key == "") and child_value == "":
        return reference.order_by_child(child_key).get()
    return reference.get()
