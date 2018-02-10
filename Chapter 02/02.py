import os, socket, threading, socketserver

SERVER_HOST = 'localhost'
SERVER_PORT = 0
BUF_SIZE = 1024

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message.encode('utf-8'))
        response = sock.recv(BUF_SIZE)
        print('Client received: %s' % response.decode())
    finally:
        sock.close()

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(BUF_SIZE)
        cur_thread = threading.current_thread()
        response = '%s; %s' % (cur_thread.name, data.decode())
        self.request.sendall(response.encode('utf-8'))
        
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':
    server = ThreadedTCPServer((SERVER_HOST, SERVER_PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target = server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print('Server loop running PID: %s' % os.getpid())
    client(ip, port, 'Hello from client 1')
    client(ip, port, 'Hello from client 2')
    client(ip, port, 'Hello from client 3')
    server.shutdown()
