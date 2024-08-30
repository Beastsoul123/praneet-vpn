import socket
import select
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
VPN_SERVER_IP = '127.0.0.1'
VPN_SERVER_PORT = 8080
VPN_SECRET_KEY = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15'
client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((VPN_SERVER_IP, VPN_SERVER_PORT))
print(f"Connected to VPN server{VPN_SERVER_IP,VPN_SERVER_PORT}")
while True:
    data = input("Enter data to send: ")
    cipher=Cipher(algorithms.AES(VPN_SECRET_KEY),modes.CBC(b'\x00'*16),backend=default_backend())
    encryptor=cipher.encryptor()
    encrypted_data = encryptor.update(data.encode()) + encryptor.finalize()
    client_socket.sendall(encrypted_data)
    response=client_socket.recv(1024)
    if response:
        decryptor = cipher.decryptor()
        decrypted_response = decryptor.update(response) + decryptor.finalize()
        print(f"Received response from VPN Server: {decrypted_response()}")
    else:
        break
client_socket.close()
