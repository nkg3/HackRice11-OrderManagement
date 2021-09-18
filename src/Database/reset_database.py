from pathlib import Path
import database

"""
Clear database and parse the entire excel file into database
"""

if __name__ == "__main__":
    database_url = 'https://hackrice11-ordermanageme-327b0-default-rtdb.firebaseio.com/'
    cred_path = Path("../DataFiles/database_private_key.json")
    excel_path = Path("../DataFiles/cheveron_data_file.xlsx")

    database.init_database(database_url, cred_path)
    database.set_with_dict({}, "/")
    database.set_with_excel(excel_path, "Equipment Details", (2, 12), (2, 9), "/equipment")
    database.set_with_excel(excel_path, "Worker Details", (1, 11), (2, 6), "/worker")
    database.set_with_excel(excel_path, "Facility Details", (2, 7), (2, 5), "/facility")
    database.set_with_excel(excel_path, "Work Order Examples", (2, 32), (2, 8), "/work_orders")
