import socket
import sys
from urllib import response

responses = []


def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    argv = sys.argv[1:]
    assert len(argv) == 2, 'You need to have at least two arguments'
    hostname = socket.gethostbyname(argv[0])
    try:
        port = int(argv[1])
    except Exception as e:
        print(e)
        exit()

    # Connect to the server
    server_binding = (hostname, port)
    cs.connect(server_binding)

    # Read lines from the text file
    hns_f = open('PROJ2-HNS.txt', 'r')
    domain_names = hns_f.readlines()
    hns_f.close()

    # Send each line to the server
    for domain_name in domain_names:
        domain_name = domain_name.strip('\n')  # get rid of \n in the end
        print(domain_name)
        cs.send(domain_name.encode('utf-8'))
        response = cs.recv(256).decode('utf-8').strip('\n')
        responses.append(response)
        print("[C]: " + response)

    cs.send("EOF".encode('utf-8'))
    cs.close()

    # Write results into file
    resolved_f = open('out-proj.txt', 'w')
    resolved_f.close()

    for r in responses:
        resolved_f = open('out-proj.txt', 'a')
        resolved_f.write(str(r)+'\n')
    resolved_f.close()

    exit()


if __name__ == "__main__":
    client()
