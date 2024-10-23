import socket
import threading

def send_message():
    while True:
        message = input("Enter the message: ")
        target_node = input("Enter the target: ")

        s = socket.socket()
        s.connect(('localhost', 5003))
        s.sendall(f"{message}|{target_node}".encode())
        
        response = s.recv(1024).decode()
        print(f"Response from {target_node}: {response}")
        s.close()

def receive_message():
    s = socket.socket()
    s.bind(('localhost', 5002))
    s.listen(5)

    while True:
        client, addr = s.accept()
        data = client.recv(1024).decode()
        message, sender_node = data.split('|')
        
        if sender_node == "Node 3":
            print(f"Message received by Node 3: {message}")
            response = f"Message displayed on Node 3"
        else:
            # print(f"Forwarding message from Node 3 to {sender_node}")
            print(f"Forwarding message from Node 3 to Node 4")
            forward_socket = socket.socket()
            forward_socket.connect(('localhost', 5003))
            forward_socket.sendall(data.encode())
            response = forward_socket.recv(1024).decode()
            forward_socket.close()

        client.sendall(response.encode())
        client.close()

if __name__ == "__main__":
    threading.Thread(target=send_message).start()
    threading.Thread(target=receive_message).start()
