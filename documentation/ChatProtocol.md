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

Messages sent between the client and server have the following form: `[command][args]`

The **command** section is a **left zero-padded string of length 10** containing the command name.

The **args** section contains the arguments to the command in the command specific format.

To initiate communication with the server, the client must send the **REGISTER** command.

Following that, the user can send and receive messages.

## Message Format

### Client Requests
| command | arguments |
| --- | --- |
| EXIT | no arguments |
| FAMILY | message |
| PRIVATE| game\_name\_to : message |
| PUBLIC | message |
| REGISTER | game\_name of the client |
| UPDATE | refresh family membership cache, resend family name |

### Server Responses
| command | arguments |
| --- | --- |
| ERROR | error number : error message |
| FAMILY | message |
| PRIVATE| game\_name\_from : game\_name\_to : message |
| PUBLIC | message |



## Error Codes
| code | message |
| :---: | --- |
| 90 | User is not online |
| 91 | Don't be an idiot |
| 80 | Your family is offline |
| 81 | You don't have a family |




## Advanced Family Chat Documentation

There is a **familyid** column in each player table which is initially set to empty string.
When the client **REGISTER**s with the server, the server will query the database for this value.
If the client's **familyid** is empty, he is not a part of any family chat.
Additionally, there is a **families** table which contains rows of family information, indexed by the unique **familyid**.


To be a part of a family, a user must either create a new family or be added to an existing one.

To create a new family, at least two family-less users are required.
The **familyid** value is taken as the game\_name of the family creator.
This value should then replace each user's **familyid** value in the database.
Also, be sure to create an entry in the **families** table containing the family name and the names of the members.

For a user to be added to an existing family chat, simply replace the user's **familyid** value with the **familyid** of the family.
Additionally, add their name to the family row in the **families** table.

To remove a user from a family chat, reset their **familyid** value to empty string, and remove their name from the family row in the **families** table.


To propagate any of these changes, the user must either log out of the chat, send the **UPDATE** command.
Changes are also propagated if any other user in the family sends the **UPDATE** command.
To ensure changes are quickly propagated, whenever a user's family status is changed, the entity which initiated the change should immediately send an **UPDATE** command.
