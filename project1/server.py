import socket


def server():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', 50007)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print("[S]: Got a connection request from a client at {}".format(addr))

    # Send a intro message to the client.
    msg = "Welcome to CS 352!"
    csockid.send(msg.encode('utf-8'))

    # Receive text from the client
    recv_msg_from_client = csockid.recv(1024).decode('utf-8')
    # Create a new file or rewrite everything from the beginning
    f = open('out-proj.txt', 'w')
    f.close()

    # Receive text from the client
    while recv_msg_from_client != "":
        reversed_msg = recv_msg_from_client[::-1]   # Reverse the text
        print("[S]: Reversing '%s' to: '%s'" %
              (recv_msg_from_client, reversed_msg))
        # Append the text to the file
        f = open('out-proj.txt', 'a')
        f.write(reversed_msg + '\n')
        csockid.send(reversed_msg.encode('utf-8'))
        recv_msg_from_client = csockid.recv(1024).decode('utf-8')
    f.close()

    print("[S]: Empty line is detected, connection closed.")

    # Close the server socket
    ss.close()
    exit()


if __name__ == "__main__":
    server()
