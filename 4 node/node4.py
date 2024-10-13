import socket

def node4():
    s = socket.socket()
    s.bind(('localhost', 5003))
    s.listen(5)
    
    while True:
        client, addr = s.accept()
        data = client.recv(1024).decode()
        message, target_node = data.split('|')
        
        if target_node == "Node 4":
            print(f"Message received by Node 4: {message}")
            response = f"Message '{message}' displayed on Node 4"
        else:
            response = "Node not found"
        
        client.sendall(response.encode())
        client.close()

if __name__ == "__main__":
    node4()
