import socket

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message:
                print(f'Client message: {message}')
            else:
                break
        except Exception:
            break

def main():
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 7560
    
    # Initialize and connect socket for the client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    
    while True:
        message = input('Enter message for client: ')
        if message.lower() == 'exit':
            print('Disconnecting from server')
            break
        else:
            client_socket.sendall(message.encode('utf-8'))
    client_socket.close()
    
    if __name__ == "__main__":
        main()