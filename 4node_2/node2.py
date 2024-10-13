import socket
import threading

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        message, target_node = data.split('|')
        
        if target_node == "Node 2":
            print(f"Message received by Node 2: {message}")
            response = f"Message '{message}' displayed on Node 2"
        else:
            forward_socket = socket.socket()
            forward_socket.connect(('localhost', 5002))
            forward_socket.sendall(data.encode())
            response = forward_socket.recv(1024).decode()
            forward_socket.close()
        
        client_socket.sendall(response.encode())

def send_messages(s):
    while True:
        message = input("Enter the message: ")
        target_node = input("Enter the target (Node 3, Node 4): ")
        s.sendall(f"{message}|{target_node}".encode())

def receive_messages(s):
    while True:
        response = s.recv(1024).decode()
        print(f"Received: {response}")

def node2():
    s = socket.socket()
    s.connect(('localhost', 5002))

    threading.Thread(target=send_messages, args=(s,)).start()
    threading.Thread(target=receive_messages, args=(s,)).start()

    server_socket = socket.socket()
    server_socket.bind(('localhost', 5001))
    server_socket.listen(5)
    
    while True:
        client, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == "__main__":
    node2()
