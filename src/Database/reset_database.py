from pathlib import Path
import database

"""
Clear database and parse the entire excel file into database set the url, credentials, and excel files use 
database.set_with_excel(<excel path>, <sheet name>, <row range (tuple)>, <col rage (tuple)>, <database dir 
reference>) 
"""

if __name__ == "__main__":
    database_url = 'https://hackrice11-ordermanageme-327b0-default-rtdb.firebaseio.com/'
    cred_path = Path("../DataFiles/database_private_key.json")  # path to database credential
    excel_path = Path("../DataFiles/cheveron_data_file.xlsx")  # path to excel sheets

    database.init_database(database_url, cred_path)
    database.set_with_excel(excel_path, "Equipment Details", (2, 12), (2, 9), "/Equipments")
    database.set_with_excel(excel_path, "Worker Details", (1, 11), (2, 7), "/Workers")
    database.set_with_excel(excel_path, "Facility Details", (2, 7), (2, 6), "/Facilities")
    database.set_with_excel(excel_path, "Work Order Examples", (2, 32), (2, 12), "/WorkOrders")
