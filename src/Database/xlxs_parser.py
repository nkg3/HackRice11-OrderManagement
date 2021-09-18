import openpyxl
from pathlib import Path

xlsx_file = Path('../test_file.xlsx')
wb = openpyxl.load_workbook(xlsx_file)
sheet = wb.active
print(sheet)