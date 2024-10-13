import socket

def node3():
    # Create a socket object to listen for connections from Node 2
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.bind(('localhost', 5003))
    s1.listen(1)
    
    conn1, addr1 = s1.accept()
    message = conn1.recv(1024).decode('utf-8')
    print(f"Node 3 received: {message}")
    conn1.close()
    
    # Now forward the message to Node 4
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect(('localhost', 5004))
    s2.sendall(message.encode('utf-8'))
    s2.close()

if __name__ == "__main__":
    node3()
