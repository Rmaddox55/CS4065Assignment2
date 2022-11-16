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
    username_taken = True
    while username_taken:
        # Receive requested username from client
        username = conn.recv(1024).decode()
        print("Client requests username " + username)

        # If username is taken, send USERNAME_TAKEN message to client
        if username in serverUsers:
            username_taken = True
            print("Requested username " + username + " is already taken. Prompting client to retry.")
            conn.send("USERNAME_TAKEN".encode())
        # If username is available, send USERNAME_ACCEPTED message to client
        else:
            username_taken = False
            serverUsers.append(username)
            print("Requested username " + username + " was available. Added " + username + " to serverUsers list." + '\n')
            conn.send("USERNAME_ACCEPTED".encode())

    # Username is now connected to server & has valid username
    # Structure to listen for commands from client
    terminate_thread = False
    while not terminate_thread:
        # Initialize client_message_list
        client_message_list = []

        # Receive message from client
        client_message = conn.recv(1024).decode()

        # Split client message into list by spaces if command isn't a post
        if client_message[0:4] != "POST":
            client_message_list = client_message.split(" ")

        # If kill signal received from client, terminate the thread
        if client_message_list[0] == "KILL":
            terminate_thread = True
            break
        # If client requests groups, send list of groups
        elif client_message_list[0] == "REQUEST_GROUPS":
            print(client_message_list[1] + " requests list of groups.")
            print("Sending number of groups to " + client_message_list[1] + ".")
            num_groups = len(groupList)
            conn.send(str(num_groups).encode())
            print("Sending list of of groups to " + client_message_list[1] + "." + '\n')
            for group_name in groupList:
                conn.send(group_name.encode())
                time.sleep(0.00005)
        # If client requests to join group, join group
        elif client_message_list[0] == "JOIN_GROUP":
            print(client_message_list[2] + " requests to join group " + client_message_list[1] + ".")
            # Check to see if client is already in group and return a message
            # Group 1 join request
            if client_message_list[1] == "1":
                if client_message_list[2] in group1Users:
                    print(client_message_list[2] + " is already in group 1." + '\n')
                    conn.send("ALREADY_JOINED_GROUP".encode())
                else:
                    group1Users.append(client_message_list[2])
                    print(client_message_list[2] + " has joined group 1." + '\n')
                    conn.send("JOINED_GROUP".encode())
            # Group 2 join request
            if client_message_list[1] == "2":
                if client_message_list[2] in group2Users:
                    print(client_message_list[2] + " is already in group 2." + '\n')
                    conn.send("ALREADY_JOINED_GROUP".encode())
                else:
                    group2Users.append(client_message_list[2])
                    print(client_message_list[2] + " has joined group 2." + '\n')
                    conn.send("JOINED_GROUP".encode())
            # Group 3 join request
            if client_message_list[1] == "3":
                if client_message_list[2] in group3Users:
                    print(client_message_list[2] + " is already in group 3." + '\n')
                    conn.send("ALREADY_JOINED_GROUP".encode())
                else:
                    group3Users.append(client_message_list[2])
                    print(client_message_list[2] + " has joined group 3." + '\n')
                    conn.send("JOINED_GROUP".encode())
            # Group 4 join request
            if client_message_list[1] == "4":
                if client_message_list[2] in group4Users:
                    print(client_message_list[2] + " is already in group 4." + '\n')
                    conn.send("ALREADY_JOINED_GROUP".encode())
                else:
                    group4Users.append(client_message_list[2])
                    print(client_message_list[2] + " has joined group 4." + '\n')
                    conn.send("JOINED_GROUP".encode())
            # Group 5 join request
            if client_message_list[1] == "5":
                if client_message_list[2] in group5Users:
                    print(client_message_list[2] + " is already in group 5." + '\n')
                    conn.send("ALREADY_JOINED_GROUP".encode())
                else:
                    group5Users.append(client_message_list[2])
                    print(client_message_list[2] + " has joined group 5." + '\n')
                    conn.send("JOINED_GROUP".encode())
        # If client requests to leave group, leave group
        elif client_message_list[0] == "LEAVE_GROUP":
            i = 0
        else:
            i = 0

    # Close connection at end of thread
    print("Client disconnected:", addr)
    conn.close()


# Main function; It controls the threads
def main():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 5000))
    s.listen(1)

    print("Server started. Waiting for clients." + '\n')
    all_threads = []

    try:
        while True:
            conn, addr = s.accept()

            print("Client connected:", addr)

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