import socket
import re
import urllib
import pickle

values = {}
HOST, PORT, REQUEST_SIZE, DICTIONARY_FILE = '', 8888, 4096, "SimpleSave.dat"

def main():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(1)
    
    try:
        with open(DICTIONARY_FILE, 'rb') as handle:
            try:
                global values
                values = pickle.loads(handle.read())
            except:
                pass
            handle.close()
    except:
        pass
    
    print values
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
    with open(DICTIONARY_FILE, 'wb') as handle:
        pickle.dump(values,handle)
        handle.close()
    
def getValue(key):
    print values
    if key in values:
        return values[key]
    else:
	return "Key Not Found"


if __name__ == "__main__":
    main()
