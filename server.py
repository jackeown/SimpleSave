#!/usr/bin/python
import socket
import re
import urllib
#import pickle
import sqlite3
#from urllib.parse import urlparse

values = {}
HOST, PORT, REQUEST_SIZE, DICTIONARY_FILE = '', 8888, 4096, "SimpleSave.db"
HTTP_200 = """HTTP/1.1 200 OK \n\n"""

def main():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(1)

    sqlConnection = sqlite3.connect(DICTIONARY_FILE)
    cursor = sqlConnection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS val (key text, val text);");
    sqlConnection.commit()
    sqlConnection.close()
    
    while True:
        client_connection, client_address = listen_socket.accept()
        request = client_connection.recv(REQUEST_SIZE)
        http_response = HTTP_200 + handleRequest(request)
        client_connection.sendall(http_response)
        client_connection.close()

def handleRequest(request):
    request = request.split(' ')[1] #remove extra HTTP headers and get only the URL data
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
	    val = setValue(key,value)
            if(isinstance(val,str)):
                return val
            else:
                return "" #Storage failed?
	else:
	    val = getValue(key)
	    if(isinstance(val,str)):
	        return val
	    else:
	        return "" #Not stored value
    return "" #No valid request?



def setValue(key,value):
    sqlConnection = sqlite3.connect(DICTIONARY_FILE)
    cursor = sqlConnection.cursor()
    t = (key, value)
    cursor.execute("INSERT OR REPLACE INTO val (key,val) VALUES (?,?);",t)
    sqlConnection.commit()
    sqlConnection.close()
    return value

def getValue(key):
    sqlConnection = sqlite3.connect(DICTIONARY_FILE)
    cursor = sqlConnection.cursor()
    t = (key,)
    cursor.execute("SELECT val FROM val WHERE key = ?;",t)
    val = cursor.fetchone()
    sqlConnection.commit()
    sqlConnection.close()
    if(val is not None):
        return str(val[0])









if __name__ == "__main__":
    main()
