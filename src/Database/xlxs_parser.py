import openpyxl
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from pathlib import Path


class ExcelParser:
    __wb: Workbook
    __sheet_names: list

    def __init__(self, path: Path):
        self.__wb = openpyxl.load_workbook(path)
        self.__sheet_names = self.__wb.sheetnames

    def parse_sheet(self, sheet_name: str, blank_row: int = 0, blank_col: int = 0) -> dict:
        if sheet_name not in self.__sheet_names:
            raise KeyError("sheet name doesn't exist")

        data: dict = {}
        sheet: Worksheet = self.__wb[sheet_name]
        rows = sheet.iter_rows(blank_row + 1, sheet.max_row, blank_col + 1, sheet.max_column)
        keys: list = []
        for i, row in enumerate(rows):
            if i == 0:
                for cell in row:
                    keys.append(cell.value)
            else:
                identifier: str = row[0].value
                data[identifier] = {}
                for j in range(len(row)):
                    data[identifier][keys[j]] = row[j].value

        return data
