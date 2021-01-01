import sqlite3 as sl

con = sl.connect('data.db')

# with con:
# 	con.execute("""
# 		CREATE TABLE DATA (
# 			key TEXT NOT NULL PRIMARY KEY,
# 			value TEXT,
# 		);
# 	""")

# sql = 'INSERT INTO DATA (key, value) values(?, ?)'
# data = [('1', 'Alice'), ('2', 'Bob'), ('3', 'Chris')]

# try:
# 	con.execute(sql, ('321', 'Alice'))
# except:
# 	print("DE")

with con:
	data = con.execute("SELECT * FROM DATA")
	for row in data:
		print(row)
print()
with con:
	data = con.execute("DELETE FROM DATA where key='dinesh'")

with con:
	data = con.execute("SELECT * FROM DATA")
	for row in data:
		print(row)