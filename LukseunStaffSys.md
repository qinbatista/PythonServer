### Lukseun Staff System

Lukseun Staff server is especially for company member, the first function is working time record, such as record the time of check in and check out,  the purpose of this server is not working for staff, if we adopt it well, our game will use the same server structure. 



### Message Logic

All data must be encrypted when server and client exchange data every time because we are using TCP to transfer data, if somebody tracks our message and simulate our message, that's very dangerous. the client must send header before sending a message, the header will tell the server "who I am" and "how many messages I have" if server recognized header, accept those quantity messages which header said. The server will send a header back too, tell the client "who I am" and "how many messages I have". client accept it and receive those message from the server.



### Encryption Method

if this message needs to be translated, server use <u>DES Encrypt</u>, if just to check message like password, server use <u>MD5</u>.



### Message Example

Client name: *"natasha"*

Client Message Content: *{"session":"ACDE48001122", "Function":"CheckTime","UserName":"abc", "Random":"774"}*

Server Message Context: *{"status":"01","message":"Check in"}*

##### 1: Create Header and send Header

###### Message example：

[Client] md5(ClientName)+size of message->[Server]7#e112b2d1f7a5fb2e316fafb6a4bf5d174e

Explain：md5 of Client name is 7e1bd1f7a5fb2e316fafb6a4bf5d174e, size of message is 122, insert size to md5 become 7`#`e`1`1`2`b`2`d1f7a5fb2e316fafb6a4bf5d174e, make sure the head always keep 36 bytes, if size not over 4 bytes, just insert # to replace number, so max size of message can be sent is <u>9999</u> bytes, it should be enough for our game.

##### 2: Analysis Header and receive a message from Client

###### Message example：

[Server]7#e112b2d1f7a5fb2e316fafb6a4bf5d174e ->[Server]app: Natasha, size:122

[Server] md5("ok")->[Client] recvied 32 bytes message, start sending message

[Client]Encrypt("{"session":"ACDE48001122", "Function":"CheckTime","UserName":"abc", "Random":"774"}")->[Server]Decrypt("{"session":"ACDE48001122", "Function":"CheckTime","UserName":"abc", "Random":"774"}")

Explain：get size from client string, the size is 122. 7e1bd1f7a5fb2e316fafb6a4bf5d174e is the md5 of Natasha, if MD5 matched, accept this request, receive remain 122 bytes message and send any 32 bytes message back to tell the client to receive message finished. If can't recognize this header, just break or don't send a message back or something safe behavior for our server.

##### 3: Make header and send Header to Client:

###### Message example：

Make header: Message example:  [Server] md5(ClientName)+size of message->[Client]7#e#15b7d1f7a5fb2e316fafb6a4bf5d174e

[Explain] same as the client, just message size changed.

##### 4: Analysis Header and recive message from Server:

###### Message example：

[Client]7`#`e#1`5`b`7`d1f7a5fb2e316fafb6a4bf5d174e ->[Client]app: Natasha, size:57

[Client] md5("ok")->[Server] recvied 32 bytes message, start sending message

[Server]Encrypt("{"status":"01","message":"Check in"}")->[Client]Decrypt("{"status":"01","message":"Check in"}")

Explain same like the client, just message changed