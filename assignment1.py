import socket
import threading

socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_port = ("localhost", 2000)
socks.connect(host_port)

def send_message():
    while True:
        message = input()
        if message == "!quit":
            break
        elif message == '!who':
            message = socks.send(("LIST\n").encode('utf-8'))
        elif message.startswith('@'):
            user, msg = message.split(' ', 1)
            socks.send(('SEND ' + user[1:] + ' ' + msg + '\n').encode('utf-8'))
        else:
            print("Invalid command. Use !quit, !who, or @username .")


def receive_message(socks):
    while True:
        try:
            msg = ""
            message = socks.recv(1024).decode('utf-8')
            if message.endswith("\n") == True:
                print(message)
            elif message.startswith("LIST"):
                print("Current users logged in: " + message)
            else:
                while (message.endswith("\n") == False):
                    msg+=message
                    message=msg
                print(message)
        except:
            print("An error occurred while receiving messages.")
            socks.close()
            break


username = input("Enter a username: ")
socks.send(("HELLO-FROM "+username+"\n").encode('utf-8'))
response = socks.recv(1024).decode('utf-8')
print("Current user logged in " + username)
if response == 'IN-USE':
    username = input("Enter a username: ")
    socks.send(username.encode('utf-8'))

receive_message_thread = threading.Thread(target=receive_message,args=(socks,))
receive_message_thread.daemon = True
receive_message_thread.start()

send_message()