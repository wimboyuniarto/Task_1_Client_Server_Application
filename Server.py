import socket
import threading

# Global dictionary to store occupancy data
occupancy_data = {}

def handle_client(client_socket):
    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break

        # Process the received data
        try:
            x, y, occupancy = map(int, data.split())
            occupancy_data[(x, y)] = occupancy
            print(f"Received occupancy data: ({x}, {y}) = {occupancy}")
        except ValueError:
            print("Invalid data format received from client")

        # Send acknowledgment to the client
        client_socket.send(b"Data received by server")

        # Print aggregated occupancy data
        print_aggregated_data()

    # Close the client socket
    client_socket.close()

def print_aggregated_data():
    print("Aggregated occupancy data:")
    for y in range(4, -1, -1):  # Iterate over rows in reverse order (from top to bottom)
        print(f"\t{y}|", end=" ")  # Print row label
        for x in range(5):  # Iterate over columns
            occupancy = occupancy_data.get((x, y), 0)  # Get occupancy value (default to 0 if not found)
            print(occupancy, end=" ")  # Print occupancy value
        print()  # Move to the next line after printing a row
    print("\t   0 1 2 3 4")  # Print column labels

def main():
    # Configure server settings
    host = '0.0.0.0'
    port = 9999

    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        # Accept incoming connection
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")

        # Handle client in a new thread
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
