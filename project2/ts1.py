import threading
import socket
import sys
import signal
import time


def ts1():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[TS1]: Server socket created")
    except socket.error as err:
        print('[TS1]: socket open error: {}\n'.format(err))
        exit()

    dns_ip = {}
    dns_type = {}

    with open('PROJ2-DNSTS1.txt', 'r') as f:
        for line in f:
            line = line.strip('\n')
            split_line = line.split(" ")
            dns_ip[split_line[0]] = split_line[1]
            dns_type[split_line[0]] = split_line[2]

    port_num = int(sys.argv[1])
    server_binding = ('',  port_num)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[TS1]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[TS1]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print("[TS1]: Got a connection request from a client at {}".format(addr))
    counter = 1
    while counter == 1:
        if csockid.fileno() == -1:
            sys.exit(0)
        query = csockid.recv(256).decode('utf-8')
        if query == 'EOF':
            break
        if query:
            for key in dns_ip:
                print(
                    "[TS1]: Matching query {0} with {1} in the table".format(query, key))
                if key.lower() == query.lower():
                    result_string = query + " " + \
                        dns_ip[key] + " " + dns_type[key] + " IN"
                    print("[TS1]: Matched! Result is " + result_string)
                    csockid.send(result_string.encode('utf-8'))
                    break
                else:
                    print("[TS1]: Not macthed")

    ss.close()
    exit()


if __name__ == "__main__":
    ts1()
