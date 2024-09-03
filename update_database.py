import csv
import sqlite3
import subprocess

conn = sqlite3.connect('db/data.db')

cursor = conn.cursor()

sql = "DELETE FROM violations"

cursor.execute(sql)

conn.commit()
conn.close()

subprocess.run(["python3", "obtenir_contrevenants_data.py"])
