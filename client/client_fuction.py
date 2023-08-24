import socket
import json
import threading


class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('127.0.0.1', 13582)
        self.client_socket.connect(self.server_address)

    def user_login(self, user_id, user_pwd):
        data = {
            'type': 'user_login',
            'content': {
                'user_id': user_id,
                'user_pwd': user_pwd
            }
        }
        json_data = json.dumps(data).encode('utf-8')
        self.client_socket.sendall(json_data)
        back_json_data = self.client_socket.recv(1024)
        back_data = json.loads(back_json_data.decode('utf-8'))
        if back_data["back_data"] == "0002":
            print("Login Success")
            return 0
        elif back_data["back_data"] == "0003":
            print("Login Failed")
            return 1

    def user_register(self, user_id, user_name, user_image, user_pwd, user_email):
        if len(user_id) > 15:
            return 2
        elif len(user_pwd) > 25 or len(user_pwd) < 6:
            return 3
        else:
            data = {
                'type': 'user_register',
                'content': {
                    'user_name': user_name,
                    'user_pwd': user_pwd,
                    'user_email': user_email,
                    'user_image': user_image,
                    'user_id': user_id
                }
            }
            json_data = json.dumps(data).encode('utf-8')
            self.client_socket.sendall(json_data)
            back_json_data = self.client_socket.recv(1024)
            back_data = json.loads(back_json_data.decode('utf-8'))
            if back_data["back_data"] == "0000":
                print("Register Success")
                return 0
            elif back_data["back_data"] == "0001":
                print("Register Fail, Sever Error")
                return 1
