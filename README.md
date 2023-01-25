# CS352
This is the collection of our independent solutions to assignments from Rutgers CS352 - Internet Technology Class in Fall 2022. The accessbility of this repository is maintained private until the end of the semester.\
### Warning
For students from the future, please do not hard copy the solution from us. If you really need help with your assignments, please read and understand the code first.
## Project 1 - Warm Up
This project includes a client and a server. The client reads text lines from a text file and sends them to the server. The server reverses the text and writes them to another text file.
## Project 2 - Asynchronous Sockets
Implementing a client sending DNS queries(client.py), a load-balancing server(ls.py), and two top-level DNS servers(ts1.py and ts2.py). The client and TSs are using socket while the LS is using selector to listen two both TSs at the same time. More information is in the pdf file in the project directory.
## Project 3 - HTTP Server with Authentication
Implementing an HTTP server that serves secret user data. Access to this secret data will be authenticated through one of two mechanisms: user name and password, and cookies presented from successful prior authentication. We will use the HTTP protocol and build simple versions of these authentication mechanisms to render browser-readable data. You will only work with one program in this project, server.py.
## Project 4 - Reliable Communication over an Unreliable Network
Implementing a reliable sender using an unreliable UDP socket. There are two programs provided in the project 4 archive: sender.py and receiver.py. You will only modify sender.py. The sender.py program is a UDP sender that must implement the techniques of reliable delivery that we discussed during lecture to upload a file to the receiver. Specifically, you will implement reliability based on stop and wait and cumulative-ACK-based selective repeat. The receiver.py program is a UDP receiver that is attempting to download a file transmitted by the sender over a lossy channel that may drop packets, ACKs, or both.
## Project - Set up your own IP network
In this project, you will set up a small IP network consisting of hosts and a router. Your network will function with full end-to-end connectivity, and you will experiment with tools like ping and traceroute.
