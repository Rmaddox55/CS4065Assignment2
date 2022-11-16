%groups:
Client sends "REQUEST_GROUPS username"
Server returns integer of number of groups, then returns all group names

%groupjoin:
Client sends "JOIN_GROUP ID username"
Server sends "JOINED_GROUP" message if user wasn't already in group
Server sends "ALREADY_JOINED_GROUP" message if user is already in group

%groupleave:
Client sends "LEAVE_GROUP ID username"
Server sends "LEFT_GROUP" message if user was in group
Server sends "NOT_IN_GROUP" message if user wasn't in group

%groupusers:
Client sends "REQUEST_USERS ID username"
Server returns users in the group

%grouppost:
Client sends "POST<>username<>ID<>SUBJECT<>BODY"




