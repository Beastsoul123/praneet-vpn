import socket
import select
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
VPN_SERVER_IP = '127.0.0.1'
VPN_SERVER_PORT = 8080
VPN_SECRET_KEY = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15'
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((VPN_SERVER_IP, VPN_SERVER_PORT))
server_socket.bind((VPN_SERVER_IP,VPN_SERVER_PORT))
server_socket.listen(5)
print(f"VPN Server listening on {VPN_SERVER_IP}:{VPN_SERVER_PORT}")
connected_clients = []
while True:
    readable, writable, errored = select.select([server_socket] + connected_clients, [], [], 0)
    for sock in readable:
        if sock in server_socket:
            client_socket, client_address = server_socket.accept()
            print(f"Connected By{client_address}")
            connected_clients.append(client_socket)
        else:
            data=sock.recv(1024)
            if data:
                cipher = Cipher(algorithms.AES(VPN_SECRET_KEY), modes.CBC(b'\x00' * 16), backend=default_backend())
                decryptor = cipher.decryptor()
                decrypted_data = decryptor.update(data) + decryptor.finalize()

                print(f"Received data from {sock.getpeername()}: {decrypted_data.decode()}")
                response=b"Hi I am your personal vpn,Care to use me!!!"
                encryptor=cipher.encryptor()
                encrypted_response = encryptor.update(response) + encryptor.finalize()
                sock.sendall(encrypted_response)
            else:
                connected_clients.remove(sock)
                sock.close()
