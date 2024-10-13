import socket
import threading

def send_messages(s):
    while True:
        message = input("Enter the message: ")
        target_node = input("Enter the target (Node 2, Node 3, Node 4): ")
        s.sendall(f"{message}|{target_node}".encode())

def receive_messages(s):
    while True:
        response = s.recv(1024).decode()
        print(f"Received: {response}")

def node1():
    s = socket.socket()
    s.connect(('localhost', 5001))

    threading.Thread(target=send_messages, args=(s,)).start()
    threading.Thread(target=receive_messages, args=(s,)).start()

if __name__ == "__main__":
    node1()
