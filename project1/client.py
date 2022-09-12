import socket
import re


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

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)

    # Receive data from the server
    data_from_server = cs.recv(128)
    print("[C]: Data received from server: {}".format(
        data_from_server.decode('utf-8')))

    #print("[C]: Input string below to get reversed, enter nothing to stop")
    #msg_from_input = str(input())
    #while msg_from_input != '':
        #cs.send(msg_from_input.encode('utf-8'))
        #reversed_str_from_server = cs.recv(1024)
        #print("[C]: Reversed message received from server: {}".format(
            #reversed_str_from_server.decode('utf-8')))
        #msg_from_input = str(input())

    #print("[C]: Empty input is detected, connection closed.")
    
    f = open('in-proj.txt','r')
    while True:
        line = f.readline()
        if line:
            cs.send(line.encode('utf-8'))
            reversed_str_from_server = cs.recv(1024)
            print(reversed_str_from_server.decode('utf-8'))
    file.close()

    # close the client socket
    cs.close()
    exit()


if __name__ == "__main__":
    client()
