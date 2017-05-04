import socket, select

# Lista para tener todas las conexiones
CONNECTION_LIST = []
# IP del Socket
TCP_IP = "127.0.0.1"
# Puerto del Socket
TCP_PORT = 1111

# AF_INET = IPv4, SOCK_STREAM = Stream de Datos
serverEnchufe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverEnchufe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverEnchufe.bind((TCP_IP, TCP_PORT))
serverEnchufe.listen(10)

# Agregar la conexion a la lista
CONNECTION_LIST.append(serverEnchufe)

while 1:
	leer_enchufe,write_enchufe,error_enchufe = select.select(CONNECTION_LIST,[],[])

	for enchufe in leer_enchufe:
		# Nueva conexion
		if enchufe == serverEnchufe:
			# Soportar nuevas conexiones
			conn, addr = serverEnchufe.accept()
			CONNECTION_LIST.append(conn)
			print "Conexion con: (%s, %s)" % addr
		# Si viene algun mensaje
		else:
			try:
				data = enchufe.recv(4096)
				if not data:
					break
				print "Mensaje recibido: " + data
				# echo the message
				enchufe.send(data)
			except:
				enchufe.close()
				CONNECTION_LIST.remove(enchufe)
				continue
serverEnchufe.close()