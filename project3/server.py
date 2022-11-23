import secrets
import socket
import signal
import sys
import random
import json

# Read a command line argument for the port where the server
# must run.
port = 8080
if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    print("Using default port 8080")

# Start a listening server socket on the port
sock = socket.socket()
sock.bind(('', port))
sock.listen(2)

# Contents of pages we will serve.
# Login form
login_form = """
   <form action = "http://localhost:%d" method = "post">
   Name: <input type = "text" name = "username">  <br/>
   Password: <input type = "text" name = "password" /> <br/>
   <input type = "submit" value = "Submit" />
   </form>
""" % port
# Default: Login page.
login_page = "<h1>Please login</h1>" + login_form
# Error page for bad credentials
bad_creds_page = "<h1>Bad user/pass! Try again</h1>" + login_form
# Successful logout
logout_page = "<h1>Logged out successfully</h1>" + login_form
# A part of the page that will be displayed after successful
# login or the presentation of a valid cookie
success_page = """
   <h1>Welcome!</h1>
   <form action="http://localhost:%d" method = "post">
   <input type = "hidden" name = "action" value = "logout" />
   <input type = "submit" value = "Click here to logout" />
   </form>
   <br/><br/>
   <h1>Your secret data is here:</h1>
""" % port

# Helper functions
# Printing.


def print_value(tag, value):
    print("Here is the", str(tag))
    print("\"\"\"")
    print(str(value))
    print("\"\"\"")
    print()

# Signal handler for graceful exit


def sigint_handler(sig, frame):
    print('Finishing up by closing listening socket...')
    sock.close()
    sys.exit(0)


    # Register the signal handler
signal.signal(signal.SIGINT, sigint_handler)


# TODO: put your application logic here!
# Read login credentials for all the users
user_f = open('passwords.txt', 'r')
users = user_f.readlines()
user_f.close()
user_pwd_database = {}
for user in users:
    user = user.strip('\n')
    user_info = user.split(' ')
    user_pwd_database[user_info[0]] = user_info[1]
print(user_pwd_database)
# Read secret data of all the users
secret_f = open('secrets.txt', 'r')
secrets = secret_f.readlines()
secret_f.close()
user_secret_database = {}
for secret in secrets:
    secret = secret.strip('\n')
    secret_info = secret.split(' ')
    user_secret_database[secret_info[0]] = secret_info[1]
print(user_secret_database)

cookie_jar = {}
cookie_flag = False
# Loop to accept incoming HTTP connections and respond.
while True:
    client, addr = sock.accept()
    req = client.recv(1024).decode("utf-8")
    print(req)

    # Let's pick the headers and entity body apart
    header_body = req.split('\r\n\r\n')
    headers = header_body[0]
    body = '' if len(header_body) == 1 else header_body[1]
    print_value('headers', headers)
    print_value('entity body', body)

    # TODO: Put your application logic here!
    # Right now, we just send the default login page.
    html_content_to_send = login_page
    headers_to_send = ''
    # But other possibilities exist, including
    # Verify cookie in the header
    result = headers.find("token=")

    if result == -1:
        html_content_to_send = login_page
        headers_to_send = ''
        cookie_flag = False
    else:
        cookie_token = str(headers[result+6:]).split('\r')[0]
        if cookie_jar.get(cookie_token) != None:
            html_content_to_send = success_page + \
                "<br/>{0}<br/>".format(
                    user_secret_database[cookie_jar[cookie_token]])
            cookie_flag = True
        else:
            print(">>>>>>bad cookie " + cookie_token)
            html_content_to_send = bad_creds_page
            cookie_flag = False

    if body == 'action=logout':
        print(">>>>>logged out")
        headers_to_send = 'Set-Cookie: token=; expires=Thu, 01 Jan 1970 00:00:00 GMT\r\n'
        html_content_to_send = logout_page
    # Body is not empty, POST and handle login information
    if not cookie_flag:
        if body != '':
            login_string = body.split('&')
            username_string = login_string[0].split('=')
            password_string = login_string[1].split('=')
            login_info = {
                username_string[0]: username_string[1],
                password_string[0]: password_string[1]
            }

            print(login_info)
            if login_info['username'] in user_pwd_database.keys():
                if user_pwd_database[login_info['username']] == login_info['password']:
                    print(">>>>>Login Successful")
                    html_content_to_send = success_page + \
                        "<br/>{0}<br/>".format(
                            user_secret_database[login_info['username']])
                    # Cookie settings
                    rand_val = random.getrandbits(64)
                    headers_to_send = 'Set-Cookie: token=' + \
                        str(rand_val) + '\r\n'
                    cookie_jar[str(rand_val)] = login_info['username']
                else:
                    print(">>>>>>Wrong password")
                    html_content_to_send = bad_creds_page
            else:
                print(">>>>>No user")
                html_content_to_send = bad_creds_page

    # html_content_to_send = logout_page

    # (2) `headers_to_send` => add any additional headers
    # you'd like to send the client?
    # Right now, we don't send any extra headers.

    # Construct and send the final response
    response = 'HTTP/1.1 200 OK\r\n'
    response += headers_to_send
    response += 'Content-Type: text/html\r\n\r\n'
    response += html_content_to_send
    print_value('response', response)
    client.send(response.encode('utf-8'))
    client.close()

    print("Served one request/connection!")
    print()

# We will never actually get here.
# Close the listening socket
sock.close()
