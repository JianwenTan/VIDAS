import socket
import sys


class TCP_IP:
    #   参数初始化
    def __init__(self):
        print("初始化成功")

    #   TCP/IP服务器端
    def Server_TCP_IP(self):
        print("服务器端口初始化")
        #   1   创建套接字 socket
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #   2   获取本地IP地址
        ip = self.get_host_ip()
        #   3   绑定本地信息 bind
        tcp_server_socket.bind(("%s" % ip, 1234))
        print("服务器IP地址：", ip)
        #   4   让默认的套接字由主动变为被动 listen
        tcp_server_socket.listen(128)

        #   服务器发送给客户端的数据
        server_to_client = [0x11, 0x11]
        server_to_client_end = [0xff, 0xff]

        while True:
            print("等待一个新的客户端")
            #   5   等待客户端的链接 accept
            new_client_socket, client_addr = tcp_server_socket.accept()

            print("一个新的客户端已经到来%s" % str(client_addr))

            #   6   为同一客户端多次服务
            while True:
                #   7   接收客户端发送过来的请求
                recv_data = new_client_socket.recv(1024)

                #   如果recv解堵塞，有以下2中方式：
                #   1.客户端发送过来数据
                #   2.客户端调用close导致而了 这里 recv解堵塞
                if hex(recv_data[0]) == '0xff' and hex(recv_data[1]) == '0xff':
                    new_client_socket.send(bytes(server_to_client_end))
                    print("客户端数据发送完毕！")
                    break
                #   接收完数据返回
                elif recv_data:
                    print("客户端发来的数据：%s" % bytes(recv_data))
                    #   回送一部分数据给客户端
                    new_client_socket.send(bytes(server_to_client))
                else:
                    print("结束！")
                    break

            #   关闭套接字
            new_client_socket.close()
            print("已经为该客户端服务完毕")
        # tcp_server_socket.close()

    #   TCP/IP客服端
    def Client_TCP_IP(self):
        print("客户端初始化")
        #   1   创建TCP的套接字
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #   客户端传输给服务器端的数据
        client_to_server0 = [0x11, 0x12, 0x13, 0x14, 0x1f]
        client_to_server1 = [0x21, 0x22, 0x23, 0x24, 0x2f]
        client_to_server2 = [0x31, 0x32, 0x33, 0x34, 0x3f]
        client_to_server3 = [0x41, 0x42, 0x43, 0x44, 0x4f]
        client_to_server4 = [0xf1, 0xf2, 0xf3, 0xf4, 0xff]
        client_to_server_end = [0xff, 0xff]

        #   客户端传输给服务器端的顺序
        client = [client_to_server0, client_to_server1, client_to_server2, client_to_server3, client_to_server4,
                  client_to_server_end]

        #   2   链接服务器
        server_addr = ("192.168.110.57", 1234)
        tcp_socket.connect(server_addr)
        #   3   循环发送消息
        while True:
            #   退出标志位清零
            exit_flag = 0
            for i in range(len(client)):
                #   发送和接受的轮数
                print("------第%s轮------" % i)
                #   发送消息
                print("发送的消息为：", bytes(client[i]))
                tcp_socket.send(bytes(client[i]))
                #   接收消息
                data = tcp_socket.recv(1024)
                print("接收的消息为：", bytes(data))
                if hex(data[0]) == '0xff' and hex(data[1]) == '0xff':
                    exit_flag = 1
            #   退出
            if exit_flag == 1:
                break

        #   4   关闭套接字
        tcp_socket.close()

    # 获取主机的IPV4地址
    def get_host_ip(self):
        #   全局定义 s
        global s
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()

        return ip

    #   代码运行
    def run(self):
        print(4)


#   程序执行
if __name__ == '__main__':
    tcp_ip = TCP_IP()
    tcp_ip.Client_TCP_IP()
    # print(tcp_ip.get_host_ip())
