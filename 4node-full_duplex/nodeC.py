import socket
import threading

# Example node map and connections (node names can be arbitrary)
node_map = {
    'A': ('localhost', 5001),
    'B': ('localhost', 5002),
    'C': ('localhost', 5003),
    'D': ('localhost', 5004)
}

# Define connections between nodes as a graph
connections = {
    'A': {'next': 'B', 'prev': 'D'},
    'B': {'next': 'C', 'prev': 'A'},
    'C': {'next': 'D', 'prev': 'B'},
    'D': {'next': 'A', 'prev': 'C'}
}

class Node:
    def __init__(self, node_name):
        self.node_name = node_name
        self.host, self.port = node_map[self.node_name]
        self.prev_node = connections[self.node_name]['prev']
        self.next_node = connections[self.node_name]['next']

    def handle_receive(self):
        """Thread to listen for incoming messages"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(5)
        
        print(f"{self.node_name} listening on {self.host}:{self.port}")
        
        while True:
            client, addr = s.accept()
            data = client.recv(1024).decode()
            message, target_node = data.split('|')
            
            if target_node == self.node_name:
                print(f"Message received by {self.node_name}: {message}")
                response = f"Message '{message}' delivered to {self.node_name}"
            else:
                # Forward the message to the next node in the path
                response = self.forward_message(data, target_node)
            
            client.sendall(response.encode())
            client.close()

    def forward_message(self, data, target_node):
        """Forwards the message to the appropriate neighboring node"""
        if target_node in node_map:
            # Based on the connections, decide where to forward the message
            # This can be based on a predefined routing table or logic
            
            if self.node_name == self.prev_node or self.node_name == self.next_node:
                forward_node = self.next_node  # Example logic; adjust as needed
            else:
                forward_node = self.prev_node  # Example logic; adjust as needed

            forward_host, forward_port = node_map[forward_node]
            forward_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            forward_socket.connect((forward_host, forward_port))
            forward_socket.sendall(data.encode())
            response = forward_socket.recv(1024).decode()
            forward_socket.close()
            return response
        else:
            return "Node not found in network."

    def send_message(self):
        """Thread for sending messages to other nodes"""
        while True:
            message = input("Enter the message: ")
            target_node = input(f"Enter the target node (known nodes: {list(node_map.keys())}): ")
            
            if target_node in node_map:
                # Start forwarding the message through the network
                forward_node = self.next_node if target_node != self.prev_node else self.prev_node
                forward_host, forward_port = node_map[forward_node]
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((forward_host, forward_port))
                s.sendall(f"{message}|{target_node}".encode())
                
                response = s.recv(1024).decode()
                print(f"Response: {response}")
                s.close()
            else:
                print("Node not found in the network")

    def start(self):
        """Start the node by launching receive and send threads"""
        receive_thread = threading.Thread(target=self.handle_receive)
        send_thread = threading.Thread(target=self.send_message)

        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()


if __name__ == "__main__":
    # Example: Initialize Node 'A'
    node = Node(node_name='C')
    node.start()
