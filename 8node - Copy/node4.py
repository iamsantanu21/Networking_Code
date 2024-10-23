import socket
import threading
import json

CURRENT_NODE = 'Node 4'
CURRENT_NODE_PORT = 5003  # Port should be an integer

def fetch_port(node):
    """Fetch the port number for a given node by reading the JSON file."""
    with open('node_ports.json', 'r') as file:
        node_data = json.load(file)
    if node in node_data:
        return node_data[node]['port']
    else:
        raise ValueError(f"Port not found for node: {node}")

def fetch_next_node(source_node, target_node):
    """Determine the next node in the path from source to target."""
    with open('node_ports.json', 'r') as file:
        node_data = json.load(file)

    # Ensure both source and target nodes exist in the data
    if source_node not in node_data or target_node not in node_data:
        raise ValueError("Source or target node not found in the node data.")

    # If the source is the same as the target, no need to forward
    if source_node == target_node:
        return source_node

    # BFS setup to find the shortest path
    queue = [(source_node, None)]  # (current node, previous node)
    visited = set()

    while queue:
        current_node, previous_node = queue.pop(0)

        if current_node == target_node:
            # If we've reached the target node, return the node leading to it
            if previous_node == source_node:
                return target_node  # Target is a direct neighbor
            return previous_node

        if current_node not in visited:
            visited.add(current_node)
            for neighbor in node_data[current_node]['connected_to']:
                if neighbor not in visited:
                    queue.append((neighbor, current_node))

    raise ValueError(f"No path found from {source_node} to {target_node}")


def send_message():
    while True:
        message = input("Enter the message: ")
        target_node = input("Enter the target node: ")
        
        s = socket.socket()
        next_node = fetch_next_node(CURRENT_NODE, target_node)
        next_node_port = fetch_port(next_node)
        s.connect(('localhost', next_node_port))
        s.sendall(f"{message}|{target_node}".encode())
        
        response = s.recv(1024).decode()
        print(f"Response from {target_node}: {response}")
        s.close()

def receive_message():
    s = socket.socket()
    s.bind(('localhost', CURRENT_NODE_PORT))
    s.listen(5)

    while True:
        client, addr = s.accept()
        data = client.recv(1024).decode()
        message, target_node = data.split('|', 1)

        if target_node == CURRENT_NODE:
            print(f"Message received by {CURRENT_NODE}: {message}")
            response = f"Message displayed on {CURRENT_NODE}"
        else:
            next_node = fetch_next_node(CURRENT_NODE, target_node)
            next_node_port = fetch_port(next_node)
            
            print(f"Forwarding message from {CURRENT_NODE} to {next_node} on port {next_node_port}")
            forward_socket = socket.socket()
            forward_socket.connect(('localhost', next_node_port))
            forward_socket.sendall(data.encode())
            response = forward_socket.recv(1024).decode()
            forward_socket.close()

        client.sendall(response.encode())
        client.close()

if __name__ == "__main__":
    threading.Thread(target=send_message).start()
    threading.Thread(target=receive_message).start()
