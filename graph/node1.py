import socket

def node1():
    # Define available nodes and their addresses
    nodes = {
        '2': ('localhost', 5002),
        '3': ('localhost', 5003),
        '4': ('localhost', 5004),
    }
    
    # Prompt the user to select the destination node
    print("Select the destination node to send the message:")
    for key in nodes.keys():
        print(f"Node {key}")
    
    destination = input("Enter the destination node number (2/3/4): ").strip()

    if destination not in nodes:
        print("Invalid node selection. Exiting.")
        return
    
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the selected node
    s.connect(nodes[destination])
    
    # Message to send
    message = f"Hello from Node 1 to Node {destination}"
    
    # Send the message
    s.sendall(message.encode('utf-8'))
    
    # Close the socket
    s.close()

if __name__ == "__main__":
    node1()
