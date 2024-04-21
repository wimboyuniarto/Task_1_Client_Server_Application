import socket
import time

def send_occupancy_data(host, port, x, y, occupancy):
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((host, port))

        # Send occupancy data to the server
        data = f"{x} {y} {occupancy}"
        client_socket.send(data.encode('utf-8'))

        # Receive acknowledgment from the server
        response = client_socket.recv(1024).decode('utf-8')
        print("Server response:", response)
    except Exception as e:
        print("Error:", e)
    finally:
        # Close the socket
        client_socket.close()

def main():
    # Server settings
    host = '127.0.0.1'  # Change this to the server's IP address
    port = 9999

    # Sample occupancy data for Sensor 1
    sensor_data_1 = [
        ([1, 2], 0),
        ([1, 3], 1),
        ([2, 2], 0),
        ([2, 3], 0)
    ]


    # Send occupancy data packages to the server for Sensor 1
    for coordinates, occupancy in sensor_data_1:
        send_occupancy_data(host, port, coordinates[0], coordinates[1], occupancy)
        time.sleep(1)  # Simulate delay between data transmissions

    # Wait for the server to process the data
    time.sleep(2)

if __name__ == "__main__":
    main()
