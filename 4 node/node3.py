import socket

def node3():
    s = socket.socket()
    s.bind(('localhost', 5002))
    s.listen(5)
    
    while True:
        client, addr = s.accept()
        data = client.recv(1024).decode()
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
        client.sendall(response.encode())
        client.close()
if __name__ == "__main__":
    node3()
