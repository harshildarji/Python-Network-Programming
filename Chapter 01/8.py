import socket

SEND_BUF_SIZE = 4096
RECV_BUF_SIZE = 16384

def modify_buff_size():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_bufsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    recv_bufsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    print('Buffer size [Before]: Send: %d; Recv: %d' % (send_bufsize, recv_bufsize))
    sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SEND_BUF_SIZE)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, RECV_BUF_SIZE)
    send_bufsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    recv_bufsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    print('Buffer size [After]: Send: %d; Recv: %d' % (send_bufsize, recv_bufsize))

if __name__ == '__main__':
    modify_buff_size()
