import socket
import os,time
import threading
import json
from user_chat import user_chat
from global_data import online_clients


def find_userid_by_socket(socket_to_find):
    for socket, userid in online_clients.items():
        if socket == socket_to_find:
            return userid
    return None  # 如果没找到对应的userid，返回None


def user_send_file(received_data, _socket, address, database):
    receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receive_socket.bind(('127.0.0.1', 0))
    ip, port = receive_socket.getsockname()
    receive_socket.listen(1)
    print(f"File server listening on {ip}:{port}")
    filepath = received_data['content']['filepath']
    filesize = received_data['content']['filesize']

    def receive_file(ip, port, filepath, _socket, receive_socket, filesize):
        message = {
            "type": "user_send_file",
            "back_data": "0000",
            "content": {
                "sender_ip": ip,
                "port": port,
                "filepath": filepath,
                "filesize": filesize
            }
        }
        json_message = json.dumps(message).encode('utf-8')
        _socket.sendall(json_message)
        client_socket, client_address = receive_socket.accept()
        print(f"已经连接上'{client_address}'，准备收取文件")
        try:
            # TODO 分离文件名字、创建目录、根据大小接受文件
            filename = os.path.basename(filepath)
            user_id = find_userid_by_socket(_socket)
            savepath = "files/" + str(user_id) + "/" + filename
            os.makedirs(os.path.dirname(savepath), exist_ok=True)  # 创建文件夹路径
            recv_data = 0
            with open(savepath, 'xb') as file:
                while True:
                    data = client_socket.recv(10240)
                    if not data:
                        print("我break了")
                        break
                    file.write(data)
                recv_data += len(data)

            print(recv_data)
            print(f"File '{savepath}' received and saved")
        except FileExistsError:
            print(f"File '{savepath}' already exists")
        except Exception as e:
            print("An error occurred:", e)
        finally:
            # user_chat(received_data, _socket, address, database)
            receive_socket.close()

    send_thread = threading.Thread(target=receive_file, args=(ip, port, filepath,_socket, receive_socket, filesize))
    send_thread.start()

    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client_socket.connect((ip, port))
    # with open(filepath, 'rb') as file:
    #     while True:
    #         data = file.read(4096)
    #         if not data:
    #             break
    #         client_socket.send(data)
    # client_socket.shutdown(socket.SHUT_WR)
    # print(f"File '{filepath}' sent")
    # client_socket.close()
