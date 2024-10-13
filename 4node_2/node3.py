import socket
import threading

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        message, target_node = data.split('|')
        
        if target_node == "Node 3":
            print(f"Message received by Node 3: {message}")
            response = f"Message '{message}' displayed on Node 3"
        else:
            forward_socket = socket.socket()
            forward_socket.connect(('localhost', 5003))
            forward_socket.sendall(data.encode())
            response = forward_socket.recv(1024).decode()
            forward_socket.close()
        
        client_socket.sendall(response.encode())

def send_messages(s):
    while True:
        message = input("Enter the message: ")
        target_node = input("Enter the target (Node 4): ")
        s.sendall(f"{message}|{target_node}".encode())

def receive_messages(s):
    while True:
        response = s.recv(1024).decode()
        print(f"Received: {response}")

def node3():
    s = socket.socket()
    s.connect(('localhost', 5003))

    threading.Thread(target=send_messages, args=(s,)).start()
    threading.Thread(target=receive_messages, args=(s,)).start()

    server_socket = socket.socket()
    server_socket.bind(('localhost', 5002))
    server_socket.listen(5)
    
    while True:
        client, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == "__main__":
    node3()
