import socket
import threading

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        message, target_node = data.split('|')
        
        if target_node == "Node 4":
            print(f"Message received by Node 4: {message}")
            response = f"Message '{message}' displayed on Node 4"
        else:
            response = "Node not found"
        
        client_socket.sendall(response.encode())

def send_messages(s):
    while True:
        message = input("Enter the message: ")
        target_node = input("Enter the target (Node 1, Node 2, Node 3): ")
        s.sendall(f"{message}|{target_node}".encode())

def receive_messages(s):
    while True:
        response = s.recv(1024).decode()
        print(f"Received: {response}")

def node4():
    s = socket.socket()
    s.connect(('localhost', 5001))  # Assuming Node4 needs to connect back to Node1

    threading.Thread(target=send_messages, args=(s,)).start()
    threading.Thread(target=receive_messages, args=(s,)).start()

    server_socket = socket.socket()
    server_socket.bind(('localhost', 5003))
    server_socket.listen(5)
    
    while True:
        client, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == "__main__":
    node4()
