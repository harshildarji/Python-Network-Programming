import os, socket, threading, socketserver

SERVER_HOST = 'localhost'
SERVER_PORT = 0
BUF_SIZE = 1024
ECHO_MSG = 'Hello echo server!'

class ForkedClient():
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))

    def run(self):
        current_process_id = os.getpid()
        print('PID %s; Sending echo message to the server: "%s"' % (current_process_id, ECHO_MSG))
        sent_data_length = self.sock.send(ECHO_MSG.encode('utf-8'))
        print('Sent: %d characters, so far...' % sent_data_length)
        response = self.sock.recv(BUF_SIZE)
        print('PID %s; Received: %s' % (current_process_id, response[5:]))

    def shutdown(self):
        self.sock.close()

class ForkingServerRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = str(self.request.recv(BUF_SIZE).encode('utf-8'))
        current_process_id = os.getpid()
        response = '%s: %s' % (current_process_id, data)
        print('Server sending response [current_process_id: data] = [%s]' % response)
        self.request.send(response.encode('utf-8'))
        return
    
class ForkingServer(socketserver.ForkingMixIn, socketserver.TCPServer,):
    pass

def main():
    server = ForkingServer((SERVER_HOST, SERVER_PORT), ForkingServerRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target = server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()
    print('Server loop running PID: %s' % os.getpid())
    client1 = ForkedClient(ip, port)
    client1.run()
    print('First client running')
    client2 = ForkedClient(ip, port)
    client2.run()
    print('Second client running')
    server.shutdown()
    client1.shutdown()
    client2.shutdown()
    server.socket.close()

if __name__ == '__main__':
    main()

