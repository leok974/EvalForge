import sqlite3

conn = sqlite3.connect('data/arcade.db')
c = conn.cursor()
c.execute("SELECT briefing_md, starter_code, objectives_json FROM questdefinition WHERE slug='sql-t2-window-functions'")
row = c.fetchone()
if row:
    print(f"Briefing: {repr(row[0])[:150]}")
    print(f"Starter: {repr(row[1])}")
    print(f"Objectives: {repr(row[2])}")
else:
    print("Not found")
