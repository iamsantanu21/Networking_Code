import socket

def node4():
    # Create a socket object to listen for connections from Node 3
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 5004))
    s.listen(1)
    
    conn, addr = s.accept()
    message = conn.recv(1024).decode('utf-8')
    print(f"Node 4 received: {message}")
    conn.close()

if __name__ == "__main__":
    node4()
