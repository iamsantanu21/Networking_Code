import socket

def node2():
    s = socket.socket()
    s.bind(('localhost', 5001))
    s.listen(5)
    
    while True:
        client, addr = s.accept()
        data = client.recv(1024).decode()
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
        client.sendall(response.encode())
        client.close()
if __name__ == "__main__":
    node2()
