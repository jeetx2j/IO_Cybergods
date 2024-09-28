import socket
import threading
import time

class Firewall:
    def __init__(self):
        self.rules = {
            'allow': [],
            'block': []
        }

    def add_rule(self, rule_type, ip, port):
        if rule_type == 'allow':
            self.rules['allow'].append((ip, port))
        elif rule_type == 'block':
            self.rules['block'].append((ip, port))

    def check_rule(self, ip, port):
        if (ip, port) in self.rules['block']:
            return False
        elif (ip, port) in self.rules['allow']:
            return True
        else:
            return False

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', 8080))
        self.server_socket.listen(5)

        print("Firewall started. Listening for incoming connections...")

        while True:
            client_socket, address = self.server_socket.accept()
            client_ip, client_port = address

            print(f"Connection from {client_ip}:{client_port}")

            if self.check_rule(client_ip, client_port):
                print(f"Allowing connection from {client_ip}:{client_port}")
                client_socket.sendall(b"Connection allowed")
            else:
                print(f"Blocking connection from {client_ip}:{client_port}")
                client_socket.sendall(b"Connection blocked")

            client_socket.close()

firewall = Firewall()
firewall.add_rule('allow', '192.168.1.100', 80)
firewall.add_rule('block', '192.168.1.200', 80)

firewall.start()