import socket


def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    # Define the port on which you want to connect to the server
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # Connect to the server on local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)

    # Receive data from the server
    data_from_server = cs.recv(128)
    print("[C]: Data received from server: {}".format(
        data_from_server.decode('utf-8')))

    # Read lines from the text file
    f = open('in-proj.txt', 'r')
    lines = f.readlines()
    # Send each line to the server
    for line in lines:
        line = line.strip('\n')  # get rid of \n in the end
        cs.send(line.encode('utf-8'))
        reversed_str_from_server = cs.recv(1024)
        print(reversed_str_from_server.decode('utf-8'))
    f.close()
    print("Done")

    # Close the client socket
    cs.close()
    exit()


if __name__ == "__main__":
    client()
