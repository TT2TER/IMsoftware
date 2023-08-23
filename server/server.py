import socket
import threading
import json
from user_register import user_register
from user_login import user_login


def process_message(message_type, information, address, conn, database):
    message_handlers = {
        'user_register': user_register,
        'user_login': user_login,
    }
    try:
        handler = message_handlers.get(message_type)
        if handler:
            succ = handler(information, address, conn, database)
            print(succ)

    except Exception as e:
        print(str(address) + " 连接异常，准备断开: " + str(e))
        # 退出用户记录
        ONLINE_USERS.remove((conn, address))
        _sql = "update login_info set is_online = 0 where ip = ?"
        c.execute(_sql, address[0].split(" "))
        database.commit()
    finally:
        try:
            conn.close()
        except:
            print(str(address) + "连接关闭异常")


def handle_client(socket, address):
    while True:
        try:
            # bufsize 指定要接收的最大数据量
            data = socket.recv(1024)
            if not data:
                break
            received_data = json.loads(data.decode('utf-8'))
            print("收到消息：", received_data)

            name = received_data['content']
            hello_msg = {'type': 'message', 'content': 'Hello' + name}
            json_data = json.dumps(hello_msg).encode('utf-8')
            socket.sendall(json_data)
        except Exception as e:
            print("连接异常，原因是：" + str(e))
        finally:
            try:
                socket.close()
            except Exception as e:
                print("socket关闭异常，原因是：" + str(e))


if __name__ == "__main__":
    try:
        # 创建socket对象
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定地址和端口
        server_address = ('127.0.0.1', 13579)
        server_socket.bind(server_address)

        # TCP 监听
        # backlog 指定在拒绝连接之前，操作系统可以挂起的最大连接数量�?
        # 该值至少为 1
        # 大部分应用程序设5就可以了
        backlog = 5
        server_socket.listen(backlog)
        print("服务器等待连接？O.o")
        while True:
            client_socket, client_address = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_handler.start()
    except Exception as e:
        print("服务器寄了，原因是：" + str(e))
