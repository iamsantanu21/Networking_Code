import socket

def node1():
    while True:
        message = input("Enter the message: ")
        
        target_node = input("Enter the target (Node 2, Node 3, Node 4): ")

        s = socket.socket()
        s.connect(('localhost', 5001))
        
        s.sendall(f"{message}|{target_node}".encode())
        
        response = s.recv(1024).decode()
        
        print(f"{response}")
        s.close()

if __name__ == "__main__":
    node1()
