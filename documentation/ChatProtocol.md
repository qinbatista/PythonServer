# Lukseun Chat Protocol

The Lukseun Chat System is built on top of TCP and uses a simple protocol to categorize transmissions.

## Game Chat Assumptions

The following list of assumptions about how the chat system will work with the game drove many of the design decisions.

There are three types of chat groups: **public**, **family**, and **private**:
- **public** chat contains all the messages of all users in the current world.
- **family** chat contains messages between friends from the same world.
- **private** chat contains messages directly between one user and another.


**public**:
- All users can see all messages

**family**:
- Only users in the same family can see these messages.
- A user can only be a part of at most one family per world.
- Initially, users are not part of any family.

**private**:
- Can only contain two users.
- Can only be seen by the participating parties.


## Protocol

The server will immediately close the client connection if an invalid message is received.

The protocol defines the max message size to be: **250 bytes**

Messages sent between the client and server have the following form: [**command**][**args**]

The **command** section is a left zero-padded string of length 10 containing the command name.

The **args** section contains the arguments to the command in the command specific format.

To initiate communication with the server, the client must send the **REGISTER** command.

Following that, the user can send and receive any number of **PUBLIC**, **FAMILY**, or **PRIVATE** messages.

## Valid Commands and Arguments


| command | arguments | client -\> server | server -\> client|
| --- | --- | :---: | :---: |
| REGISTER | game\_name of the client | 是 | 否  |
| PUBLIC | message | 是 | 是 |
| FAMILY | message | 是 | 是 |
| PRIVATE| game\_name\_recipient **:** message | 是 | 是 |
| EXIT | no arguments | 是 | 否 |
| ERROR | error message | 否 | 是 |
| UPDATE | re-read the family id from database | 是 | 否 |





## Advanced Family Chat Documentation

There is a **familyid** column in each player table which is initially set to empty string.
When the client **REGISTER**s with the server, the server will query the database for this value.
If the client's **familyid** is empty, he is not a part of any family chat.

To be a part of a family, a user must either create a new family or be added to an existing one.

To create a new family, at least two family-less users are required.
The **familyid** value is taken as the game\_name of the family creator.
This value should then replace each user's **familyid** value in the database.

For a user to be added to an existing family chat, simply replace the user's **familyid** value with the **familyid** of the family.

To remove a user from a family chat, reset their **familyid** value to empty string.
To propagate these changes, the user must either log out of the chat or send the **UPDATE** command.
The ensure changes are quickly propagated, whenever a user's family status is changed, the entity which initiated the change should immediately send an **UPDATE** command.
