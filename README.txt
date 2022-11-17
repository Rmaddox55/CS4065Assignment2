PROTOCOL DESIGN: 
The client and server communicate through plain text message strings that symbolize codes. Each command the client enters will trigger the client to send a code to the server, which returns a code to the client based on the result of the command. 



COMMANDS & CODES:
%exit
Client sends "KILL" to the server to let server know that client is terminating connection
Server triggers a boolean value to terminate the client thread

%groups:
Client sends "REQUEST_GROUPS username"
Server sends an integer of the number of groups to client
Server then sends each group name to the client

%groupjoin:
Client sends "JOIN_GROUP ID username"
Server sends "JOINED_GROUP" message to client if user wasn't already in group
Server sends "ALREADY_JOINED_GROUP" message to if user is already in group

%groupleave:
Client sends "LEAVE_GROUP ID username"
Server sends "LEFT_GROUP" message to client if user was in group
Server sends "NOT_IN_GROUP" message to client if user wasn't in group

%groupusers:
Client sends "REQUEST_USERS ID username"
If client has joined specified group ID:
	Server sends "FETCHING_USERS" message to client
	Server sends an integer of the number of users in the group to client
	Server sends users in group ID specified to client
If client has not joined specified group ID:
	Server sends "NOT_IN_GROUP" message if user is not in the group

%grouppost:
Client sends "POST<>username<>ID<>SUBJECT<>BODY"




