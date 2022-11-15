# Server.py
# By: Reagan Maddox & Trung Nguyen
# Starter Code: https://stackoverflow.com/questions/68425239/how-to-handle-multithreading-with-sockets-in-python

import socket
import threading
import time

# Global variables that act as data storage of server
# serverUsers - stores each username submitted to server
# groupList - stores the name of each different message board
# groupXUsers - stores the users of each message board in the order that they joined
# groupXSubjects - stores the subjects of each message posted in order
# groupXMessages - stores the content of each post in order
# groupXPosters - stores the poster of each post in order
serverUsers = []
groupList = ["Group 1", "Group 2", "Group 3", "Group 4", "Group 5"]
group1Users = []
group1Subjects = []
group1Messages = []
group1Posters = []
group2Users = []
group2Subjects = []
group2Messages = []
group2Posters = []
group3Users = []
group3Subjects = []
group3Messages = []
group3Posters = []
group4Users = []
group4Subjects = []
group4Messages = []
group4Posters = []
group5Users = []
group5Subjects = []
group5Messages = []
group5Posters = []


# Function that is the driver of the server program; It handles the commands
def handle_client(conn, addr):
    # Loop until a non-taken username is entered
    usernameTaken = True
    while usernameTaken == True:
        # Receive requested username from client
        username = conn.recv(1024).decode()
        username = username.lower()
        print("Client requests username " + username)

        # Send USERNAME_TAKEN to client if username is taken
        if username in serverUsers:
            usernameTaken = True
            print("Requested username " + username + " is already taken. Prompting client to retry.")
            conn.send("USERNAME_TAKEN".encode())
        # Send USERNAME_ACCEPTED to client and add username to serverUsers list if not taken
        else:
            usernameTaken = False
            serverUsers.append(username)
            print("Requested username " + username + " is available. Added to serverUsers list.")
            conn.send("USERNAME_ACCEPTED".encode())

    # recv message
    # print("[thread] client:", addr, 'recv:', message)

    # send answer
    # message = "Bye!"
    # message = message.encode()
    # conn.send(message)
    # print("[thread] client:", addr, 'send:', message)

    conn.close()


# Main function; It controls the threads
def main():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 5000))
    s.listen(1)

    all_threads = []

    try:
        while True:
            print("Waiting for client")
            conn, addr = s.accept()

            print("Client:", addr)

            t = threading.Thread(target=handle_client, args=(conn, addr))
            t.start()

            all_threads.append(t)
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")
    finally:
        if s:
            s.close()
        for t in all_threads:
            t.join()


if __name__ == '__main__':
    main()