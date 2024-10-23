import socket
import threading
import json

CURRENT_NODE = 'Node 3' 
CURRENT_NODE_PORT = 5002 

def fetch_port(node):
    with open('node_ports.json', 'r') as file:
        node_data = json.load(file)
    if node in node_data:
        return node_data[node]['port']
    else:
        raise ValueError(f"Port not found for node: {node}")

def fetch_next_node(source_node, target_node):
    with open('node_ports.json', 'r') as file:
        node_data = json.load(file)

    if source_node not in node_data or target_node not in node_data:
        raise ValueError("Source or target node not found in the node data.")

    if source_node == target_node:
        return source_node

    queue = [(source_node, [source_node])] 
    visited = set()

    while queue:
        current_node, path = queue.pop(0)

        if current_node == target_node:
            return path[1] if len(path) > 1 else target_node

        if current_node not in visited:
            visited.add(current_node)
            for neighbor in node_data[current_node]['connected_to']:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

    raise ValueError(f"No path found from {source_node} to {target_node}")


def send_message():
    while True:
        message = input("Enter the message: ")
        target_node = input("Enter the target node: ")

        s = socket.socket()
        try:
            next_node = fetch_next_node(CURRENT_NODE, target_node)
            next_node_port = fetch_port(next_node)
            s.connect(('localhost', next_node_port))
            s.sendall(f"{message}|{target_node}".encode())

            response = s.recv(1024).decode()
            print(f"Response from {next_node}: {response}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
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

            # Log forwarding message
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
