import socket
def main():
    HOST = 'your_public_ip' # Replace with your public IP address
    PORT = 12345 # Replace with your desired port

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    
    while True:
        message = input('Enter message to send: ')
        client_socket.sendall(message.encode('utf-8'))
        if message.lower() == 'exit':
            print('Disconnecting from server')
            break
    # To get server response
        data = client_socket.recv(1024).decode('utf-8')
        print(f'Server response: {data}')