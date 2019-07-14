# Aliya Server System

The Aliya server system has been rebuilt from the ground up with Python's asyncio functionality in mind. Nearly all of the server side function calls use asyncio libraries to interract with either an SQL database, or HTTP requests/responses. The current server system is broken up into several distinct parts; each part managing its own resource. The system has three main components: the lukseun\_server, the token\_server, and several "Managers".


## Lukseun\_server

This component serves as the gateway between client requests, and our internal server network. Client requests are made using low level TCP streams, while internal network requests are made using HTTP. The TCP protocol is as follows: first send a fixed sized header containing the MD5 hash value of 'aliya' followed by a left zero-padded number corresponding to the size of the message to follow. Each side verifies that the header is of valid format, and then continues to read the remainder of the message. If the header does is not of valid format, simply close the connection. The message following the header is first encrypted via DES, and then base64 encoded.


#### Example valid header
A valid header for a message payload size of 10 bytes:

36 Bytes: [  aliya\_md5 value (32 bytes)  ] + [ 0010 (remaining 4 bytes) ]

Notice the left zero-padded size value comprising of the last 4 bytes of the header.

#### Standard Message Format

All messages sent to and from the server follow a standard format:

Client to Server Request: 
```json
{
	"function" : "The name of the function you want to call",
  "random":"253",
	"data" : {
				"key" : "value"
			 }
}
```


Server to Client Response: 
```json
{
	"status" : "status number",
	"message" : "message of status",
  "random":"253",
	"data" : {
				"key" : "value"
			 }
}
```


The payload within the "data" field changes depending upon the function you wish to call.


## Token\_server

The token server generates valid tokens for users, as well as verify their validity. All function calls, unless explicitly marked otherwise, require a valid token to be present in the "data" payload of the request. The token server currently issues JWT (Json Web Tokens) which can be partially decoded (base64url) from the client side to reveal the unique\_id of the issued user. Direct client requests to the token server are typically not made. Instead, the lukseun server will make requests to the token server when it receives a request from the client.


## Managers

A manager is a standalone HTTP server which maintains persistent connections to the SQL database, and provides a simple HTTP API to make requests. These managers are not exposed to the internet - they are strictly for use on our private network by our trusted servers. All requests to Managers assume that the user is properly authorized. This means that it is the Lukseun\_server's responsibility to check that a valid token has been provided in the client request before forwarding the request to the appropriate Manager. Each Manager is responsible for one type of thing, and that thing only. For example, the BagManager is responsible for the user's bag. Requests to check how many coins are present, or requests to remove coins from the user's bag should all be made to the BagManager. Similarly, all requests related to weapons should be made to the WeaponManager. If the WeaponManager needs to access bag data to perform a task, it should make a requestto the BagManager itself.


## API Documentation

See each respective Manager documentation for example API calls.
