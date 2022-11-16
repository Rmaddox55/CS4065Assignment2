# Client.py
# By: Reagan Maddox & Trung Nguyen
# Send data    --> client_socket.send(message.encode())
# Receive data --> data = client_socket.recv(1024).decode()
# command[0:4] -> first 4 characters of command

import socket
import time

# Function that prints out the help menu for the client program
def help_menu():
    print('Available Commands:')
    print('"%groups"                         <--- Prints a list of all message board groups')
    print('"%groupjoin GroupID"              <--- Joins the group specified GroupID integer')
    print('"%groupleave GroupID"             <--- Leaves the group with specified GroupID integer')
    print('"%groupusers ID"                  <--- Prints a list of users belonging to the group with specified ID')
    print('"%grouppost ID SUBJECT<>BODY"     <--- Posts to the message board with subject and message to the corresponding group ID')
    print('"%groupmessage GroupID MessageID" <--- Retrieves a specified message ID from specified group ID')
    print('"%exit"                           <--- Terminates client program' + '\n')


# Driver function of the client program
def main():
    a = "POST<>username<>ID<>SUBJECT<>BODY"
    print(a[0:4])

    # Initialize boolean that terminates program
    terminate_program = False

    # Initialize socket
    client_socket = socket.socket()

    # Print available command
    print('Available Commands:')
    print('"%connect IPAddress PortNumber"   <--- Connects to a server using specified IP address & port number')
    print('"%exit"                           <--- Terminates client program' + '\n')

    # Initialize parameters for %connect
    username = ""
    command = ""
    ip_address = ""
    port_number = ""

    # Loop through until correct command is entered to establish connection to server
    while command != "%connect" and (not terminate_program):
        command = input("Enter a command: ")

        command_list = command.split(" ")
        if len(command_list) == 3:
            command = command_list[0]
            ip_address = command_list[1]
            port_number = command_list[2]

        # Check different parts of command for validity
        if (command == "%connect") and (ip_address == "127.0.0.1") and (port_number == "5000"):
            # If input is good, connect to server
            client_socket.connect((ip_address, int(port_number)))
            print("Connected to " + ip_address + ":" + port_number + '\n')
        else:
            # If input is bad, find incorrect parts and print to user
            if command == "%connect":
                if ip_address != "127.0.0.1":
                    print("Invalid IP address.")
                if port_number != "5000":
                    print("Invalid port number.")
                command = ""
            # Terminate program on exit command
            elif command == "%exit":
                terminate_program = True
            # Invalid command, reset for next loop iteration
            else:
                print("Invalid command.")
                command = ""
            print(" ")

    # Prompt user to enter an alpha username and send to server to check if available
    server_message = ""
    while (server_message != "USERNAME_ACCEPTED") and (not terminate_program):
        username = input("Enter a username to use on this server: ")
        username = username.capitalize()

        if not username.isalpha():
            print("Username must only contain letters. No numbers, special characters, or spaces are allowed. Invalid Username.")
        else:
            client_socket.send(username.encode())
            server_message = client_socket.recv(1024).decode()
            if server_message != "USERNAME_ACCEPTED":
                print("Username is already taken. Please try a different username.")
            else:
                print("Username has been accepted. Your username on this server is " + username + "." + "\n")

    # Print menu of available commands now that user has joined the server with valid username
    if not terminate_program:
        help_menu()

    # Looping structure that loops until %exit command is entered
    while not terminate_program:
        # Take command input
        command = input("Enter a command: ")

        # Split command into chunks by blank space
        command_list = command.split(" ")

        # If-Structure for every valid command
        # End program on %exit command
        if command_list[0] == "%exit":
            terminate_program = True
            client_socket.send(("KILL " + username).encode())
            break
        # Print out groups retrieved from server
        elif command_list[0] == "%groups":
            print("Requesting list of groups from server.")
            print("Server Groups:")
            client_socket.send(("REQUEST_GROUPS " + username).encode())
            num_groups = int(client_socket.recv(1024).decode())
            i = 1
            while i < (num_groups + 1):
                group_name = client_socket.recv(1024).decode()
                print(str(i) + " - " + group_name)
                i = i + 1
            print("")
        # Request to join group on %groupjoin command
        elif command_list[0] == "%groupjoin":
            # Valid group IDs
            if command_list[1] == "1" or command_list[1] == "2" or command_list[1] == "3" or command_list[1] == "4" or command_list[1] == "5":
                print("Requesting to join group " + command_list[1] + ".")
                client_socket.send(("JOIN_GROUP " + command_list[1] + " " + username).encode())
                server_message = client_socket.recv(1024).decode()
                if server_message == "JOINED_GROUP":
                    print("Successfully joined group " + command_list[1] + "." + '\n')
                if server_message == "ALREADY_JOINED_GROUP":
                    print("You are already in group " + command_list[1] + "." + '\n')
            else:
                print("Couldn't join group. Invalid group number.")
        else:
            print("Invalid command.")

    # Close socket to end connection
    print("Client program is terminating. ")
    client_socket.close()


if __name__ == '__main__':
    main()