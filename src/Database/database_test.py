import firebase_admin
from firebase_admin import db
import json
from pathlib import Path

database_url = 'https://hackrice11-ordermanageme-327b0-default-rtdb.firebaseio.com/'
path = Path("../DataFiles/database_private_key.json")
cred = firebase_admin.credentials.Certificate(path)
default_app = firebase_admin.initialize_app(cred, {'databaseURL': database_url})

ref = db.reference("/")

with open("../DataFiles/test_data.json", "r") as data:
    content = json.load(data)

ref.set(content)