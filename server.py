import json
import socket               # Import socket module
import sqlite3 as sl

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.


con = sl.connect('data.db')

with con:
	con.execute("""
		CREATE TABLE IF NOT EXISTS DATA (
			key TEXT NOT NULL PRIMARY KEY,
			value TEXT
		);
	""")


read, write = False, False


def createData(c, data):
	global read, write
	if (read == True or write == True): c.send(b'err: Data already in read/write mode')
	else:
		write = True

		sql = "INSERT INTO DATA (key, value) values('"+data[0]+"', '"+data[1]+"')"
		try:
			con.execute(sql); con.commit();
			c.send(b'info: Data successfully created')
			print("createData:", {data[0], data[1]})
		except:
			c.send(b'err: Key already exists')
			print("createData:", "Key already exists")

		write = False


def readData(c, data):
	global read, write
	if (write == True): c.send(b'err: Data is in write mode in another process')
	else:
		# print(data)
		read = True
		
		qry = "SELECT * FROM DATA WHERE key='"+data+"'"
		row = con.execute(qry)
		row = list(row)

		if (len(row) == 0): 
			c.send(b'err: Data doesn\'t exists')
			print("readData  :", "Data doesn\'t exists")
		else: 
			c.send(('Value: '+str(row[0][1])).encode('utf-8'))
			print("readData  :", "{"+data+", "+row[0][1]+"}")

		read = False

def deleteData(c, data):
	global read, write
	if (read == True or write == True): c.send(b'err: Data already in read/write mode')
	else:
		write = True

		try:
			sql = "SELECT * from DATA where key='"+data+"'"
			res = con.execute(sql);
			l = list(res)

			if (len(l) == 0):
				c.send(b'err: Key doesn\'t exists')
				print("deleteData:", "Key doesn\'t exists")
			else:
				sql = "DELETE FROM DATA where key='"+data+"'"
				con.execute(sql); con.commit();
				c.send(b'info: Data successfully Deleted')
				print("deleteData:", data)

		except:
			c.send(b'err: DB connection error')
			print("deleteData:", "DB connection error")

		write = False


print("[Server Started]\n")

c, addr = s.accept()

while True:

	data = c.recv(1024)
	if(data == b''):
		c.close()
		c, addr = s.accept()
		continue
	
	data = json.loads(data)
	optype = data['type']

	if (optype == "create"): createData(c, data['data'])
	elif (optype == "read"): readData(c, data['data'])
	elif (optype == "delete"): deleteData(c, data['data'])
	elif (optype == "stopServer"):
		c.send(b'\nServer Stopped\n')
		break


c.close()
con.close()

print("\n[Server Stopped]\n")