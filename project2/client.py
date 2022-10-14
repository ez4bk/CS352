import socket
import sys

responses = []


def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    # Define the port on which you want to connect to the server
    argv = sys.argv[1:]
    assert len(argv) == 2, 'You need to have at least two arguments'
    hostname = argv[0]
    try:
        port = int(argv[1])
    except Exception as e:
        print(e)
        exit()

    # Connect to the server on local machine
    server_binding = (hostname, port)
    cs.connect(server_binding)

    # Receive data from the server
    hello_msg = cs.recv(256)
    print("[C]: Data received from server: {}".format(
        hello_msg.decode('utf-8')))

    # Read lines from the text file
    hns_f = open('PROJ2-HNS.txt', 'r')
    domain_names = hns_f.readlines()
    # Send each line to the server
    for domain_name in domain_names:
        domain_name = domain_name.strip('\n')  # get rid of \n in the end
        cs.send(domain_name.encode('utf-8'))
        ip_addr = cs.recv(256).decode('utf-8').strip('\n')
        response = "{0}\t{1}\tA\tIN".format(domain_name, ip_addr)
        responses.append(response)
        print("[C]: " + response)
    hns_f.close()

    resolved_f = open('out-proj.txt', 'w')
    resolved_f.close()

    for r in responses:
        resolved_f = open('out-proj.txt', 'a')
        resolved_f.write(str(r)+'\n')
        # Close the client socket
    resolved_f.close()

    cs.close()
    exit()


if __name__ == "__main__":
    client()
