import socket
import threading

def send_message():
    while True:
        target_node = input("Enter the target node (Node 1, Node 2, Node 3, Node 4): ")
        message = input("Enter the message: ")
        
        node_address = {
            "Node 1": ('localhost', 5000),
            "Node 2": ('localhost', 5001),
            "Node 3": ('localhost', 5002),
            "Node 4": ('localhost', 5003)
        }
        
        if target_node in node_address:
            try:
                s = socket.socket()
                next_node_address = get_next_node(node_name, target_node)
                s.connect(next_node_address)
                s.sendall(f"{message}|{target_node}|{node_name}".encode())  # Include origin node
                response = s.recv(1024).decode()
                print(f"Response from {target_node}: {response}")
                s.close()
            except Exception as e:
                print(f"Error sending message to {target_node}: {e}")
        else:
            print(f"Invalid target node: {target_node}")

def receive_message(port, node_name):
    s = socket.socket()
    s.bind(('localhost', port))
    s.listen(5)
    print(f"{node_name} is listening on port {port}...")
    
    while True:
        client, addr = s.accept()
        data = client.recv(1024).decode()
        message, target_node, origin_node = data.split('|')
        
        if target_node == node_name:
            print(f"Message received by {node_name}: {message}")
            response = f"Message '{message}' displayed on {node_name}"
        else:
            forward_to = get_next_node(node_name, target_node)
            if forward_to:
                print(f"{node_name} forwarding message to {forward_to} (for {target_node})")  # Log forwarding
                forward_socket = socket.socket()
                forward_socket.connect(forward_to)
                forward_socket.sendall(f"{message}|{target_node}|{origin_node}".encode())
                response = forward_socket.recv(1024).decode()
                forward_socket.close()
            else:
                response = "Node not found"
        
        client.sendall(response.encode())
        client.close()

def get_next_node(current_node, target_node):
    # Define the bidirectional path-based routing
    path = {
        # Forward path
        "Node 1": "Node 2",
        "Node 2": "Node 3",
        "Node 3": "Node 4",
        
        # Reverse path
        "Node 4": "Node 3",
        "Node 3": "Node 2",
        "Node 2": "Node 1"
    }
    
    node_address = {
        "Node 1": ('localhost', 5000),
        "Node 2": ('localhost', 5001),
        "Node 3": ('localhost', 5002),
        "Node 4": ('localhost', 5003)
    }
    
    next_node = path.get(current_node)
    
    if next_node and next_node in node_address:
        return node_address[next_node]
    
    return None

if __name__ == "__main__":
    node_name = input("Enter the name of this node (Node 1, Node 2, Node 3, Node 4): ")
    port = int(input(f"Enter the port for {node_name} (5000-5003): "))
    
    receiver_thread = threading.Thread(target=receive_message, args=(port, node_name))
    sender_thread = threading.Thread(target=send_message)
    
    receiver_thread.start()
    sender_thread.start()
    
    receiver_thread.join()
    sender_thread.join()
