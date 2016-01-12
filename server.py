import socket
import re
import urllib
values = {}

def main():
    HOST, PORT, REQUEST_SIZE = '', 8888, 4096

    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(1)
    while True:
        client_connection, client_address = listen_socket.accept()
        request = client_connection.recv(REQUEST_SIZE)
        http_response = """HTTP/1.1 200 OK \n\n"""+handleRequest(request)
        client_connection.sendall(http_response)
        client_connection.close()

def handleRequest(request):
    request = request.split(' ')[1] #remove extra HTTP headers and get only URL data
    request = re.split("&|\?",request)
    key = False
    value = False
    for i in request:
	if i[0:4] == "key=":
            key = urllib.unquote(i[4:])
	elif i[0:6] == "value=":
	    value = urllib.unquote(i[6:])
    if isinstance(key,str):
	if isinstance(value,str):
	    setValue(key,value)
	else:
	    return getValue(key)
    return ''


def setValue(key,value):
    values[key]=value
def getValue(key):
    if key in values:
        return values[key]
    else:
	return "Key Not Found"


if __name__ == "__main__":
    main()
