# Erik Razo
# Lab 7 - SQLite Database

import sqlite3

# Create database
con = sqlite3.connect('razo.db')
cur = con.cursor()

# Create table
cur.execute('''
CREATE TABLE IF NOT EXISTS PopByRegion (
    Region TEXT,
    Population INTEGER
)
''')

# Insert data
cur.execute("INSERT INTO PopByRegion VALUES ('Central Africa', 330993)")
cur.execute("INSERT INTO PopByRegion VALUES ('Southeastern Africa', 743112)")
cur.execute("INSERT INTO PopByRegion VALUES ('Japan', 100562)")

# Save changes
con.commit()

# Close connection
cur.close()
con.close()

"""
----- SQLITE SESSION OUTPUT -----

>>> import sqlite3
>>> con = sqlite3.connect('razo.db')
>>> cur = con.cursor()

>>> cur.execute('SELECT Region, Population FROM PopByRegion')
>>> cur.fetchall()
[('Central Africa', 330993), ('Southeastern Africa', 743112), ('Japan', 100562)]

>>> cur.execute('SELECT Region, Population FROM PopByRegion ORDER by Region')
>>> cur.fetchall()
[('Central Africa', 330993), ('Japan', 100562), ('Southeastern Africa', 743112)]

>>> cur.execute('SELECT Region FROM PopByRegion')
>>> cur.fetchall()
[('Central Africa',), ('Southeastern Africa',), ('Japan',)]

>>> cur.execute('SELECT Region FROM PopByRegion WHERE Population > 400000')
>>> cur.fetchall()
[('Southeastern Africa',)]

>>> cur.execute('SELECT * FROM PopByRegion WHERE Region = "Japan"')
>>> cur.fetchone()
('Japan', 100562)

>>> cur.execute('UPDATE PopByRegion SET Population = 100600 WHERE Region = "Japan"')

>>> cur.execute('SELECT * FROM PopByRegion WHERE Region = "Japan"')
>>> cur.fetchone()
('Japan', 100600)

>>> cur.execute('DELETE FROM PopByRegion WHERE Region < "S"')

>>> cur.execute('SELECT * FROM PopByRegion')
>>> cur.fetchall()
[('Southeastern Africa', 743112)]

>>> cur.close()
>>> con.close()

"""
