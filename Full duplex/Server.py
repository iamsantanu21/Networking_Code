import socket
import threading

# Constants
HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Port to listen on

def handle_client(client_socket):
    """Function to handle receiving messages from the client."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Client: {message}")
        except ConnectionResetError:
            break

    print("Client disconnected.")
    client_socket.close()

def main():
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the address and port
    server_socket.bind((HOST, PORT))
    
    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server waiting for client on port {PORT}...")

    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()
    print(f"Client connected: {client_address}")

    # Create a thread to handle incoming messages from the client
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()

    # Main loop to send messages to the client
    while True:
        try:
            user_input = input()
            if user_input:
                client_socket.sendall(user_input.encode('utf-8'))
        except BrokenPipeError:
            break

    # Clean up
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
