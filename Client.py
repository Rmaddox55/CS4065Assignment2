# Client.py
# By: Reagan Maddox & Trung Nguyen
# Send data    --> client_socket.send(message.encode())
# Receive data --> data = client_socket.recv(1024).decode()

import socket


# Function that prints out the help menu for the client program
def help_menu():
    print('Available Commands:')
    print('"%groups"                         <--- Prints a list of all message board groups')
    print('"%groupjoin GroupID"              <--- Joins the group specified GroupID integer')
    print('"%grouppost ID SUBJECT:BODY"      <--- Posts to the message board with subject and message to the corresponding group ID')
    print('"%groupusers ID"                  <--- Prints a list of users belonging to the group with specified ID')
    print('"%groupleave ID"                  <--- Leaves the group with specified ID')
    print('"%groupmessage GroupID MessageID" <--- Retrieves a specified message ID from specified group ID')
    print('%exit                             <--- Terminates client program' + '\n')


# Driver function of the client program
def main():
    # Initialize boolean that kills program
    killProgram = False

    # Print available command
    print('Available Commands:')
    print('%connect IPAddress PortNumber     <--- Connects to a server using specified IP address & port number')
    print('%exit                             <--- Terminates client program' + '\n')

    command = ""
    ipAddress = ""
    portNumber = ""

    # Loop through until correct command is entered to establish connection to server
    while (command != "%connect") and (killProgram == False):
        command = input("Enter a command to establish a connection to a server: ")

        inputList = command.split(" ")
        if len(inputList) == 3:
            command = inputList[0]
            ipAddress = inputList[1]
            portNumber = inputList[2]

        # Check different parts of command for validity
        if (command == "%connect") and (ipAddress == "127.0.0.1") and (portNumber == "5000"):
            # If input is good, connect to server
            client_socket = socket.socket()
            client_socket.connect((ipAddress, int(portNumber)))
            print("Connected to " + ipAddress + ":" + portNumber + '\n')

        else:
            # If input is bad, find incorrect parts and print to user
            if command == "%connect":
                if ipAddress != "127.0.0.1":
                    print("Invalid IP address.")
                if portNumber != "5000":
                    print("Invalid port number.")
                command = ""
            elif command == "%exit":
                killProgram = True
            else:
                print("Invalid command.")
                command = ""

    # Prompt user to enter a username and send to server to check validity
    serverMessage = ""
    while serverMessage != "USERNAME_ACCEPTED":
        username = input("Enter a username to use on this server: ")
        if username[0] == "%":
            print("Username cannot start with a %. Invalid Username.")
        else:
            client_socket.send(username.encode())
            serverMessage = client_socket.recv(1024).decode()
            if serverMessage != "USERNAME_ACCEPTED":
                print("Username is already taken. Please try a different username.")
            else:
                print("Username has been accepted. Your username on this server is " + username.lower() + "." + "\n")

    # Print menu of available commands now that user has joined the server with valid username
    help_menu()

    # Here is some comments to make a gap before end of program
    # 1
    # 1
    # 1
    client_socket.close()


if __name__ == '__main__':
    main()