import socket

def print_machine_info():
    host_name = socket.gethostname()
    ip_addr = socket.gethostbyname(host_name)
    print('Host name: %s\nIP address: %s' % (host_name, ip_addr))

if __name__ == '__main__':
    print_machine_info()
