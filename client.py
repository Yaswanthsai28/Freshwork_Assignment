import json
import socket

s = socket.socket()
host = socket.gethostname()
port = 12345
s.connect((host, port))

while(True):
	
	print("Select CRD Options:")
	print("\t1) Create\n\t2) Read\n\t3) Delete\n\t4) Exit\n\t5) Stop Server\n\nOption: ", end='')
	option = input()

	if (option == "1"):
		key = input("Enter Key: ")
		val = input("Enter Value: ")

		s.send(json.dumps({"type": "create", "data": [key, val]}).encode('utf-8'))
		print("\n"+s.recv(1024).decode("utf-8")+"\n")


	elif (option == "2"):
		key = input("Enter Key: ")
		
		s.send(json.dumps({"type": "read", "data": key}).encode('utf-8'))
		print("\n"+s.recv(1024).decode("utf-8")+"\n")

	elif (option == "3"):
		key = input("Enter Key: ")

		s.send(json.dumps({"type": "delete", "data": key}).encode('utf-8'))
		print("\n"+s.recv(1024).decode("utf-8")+"\n")

	elif (option == "4"): break
	elif (option == "5"):
		s.send(json.dumps({"type": "stopServer"}).encode('utf-8'))
		print("\n"+s.recv(1024).decode("utf-8")+"\n")
		break
	else: print("\nEnter correct option...")

s.close()