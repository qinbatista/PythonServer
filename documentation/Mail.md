# Mail

Mail is responsible for handling all requests pertaining to the user's mailbox.
A user's mailbox can contain announcements to all the players, friend requests, and gift items from other players.
The mailbox is different per world.

Internally, the mailbox stores mail on disk in the standard email Maildir format.
The Maildir format does not use a database to manage files, rather it uses a directory structure to organize mail.


See the General Server documentation for more information on request and response format.


# General API Documentation


To be described later

Standard mail response json format.
All mail returned by the server to the client will follow this format.

**data** contains optional key value pairs depending upon the type of the message.

```json
{
	"time" : time message was received at the server - str,
	"from" : account name of the sender - str,
	"body" : the body of the message - str,
	"type" : the type of the message - str,
	"data" :
	{
		key-value pairs depending upon the type of the message
	},
	"subject" : the subject of the message - str
}
```




# Public

## ========   get all mail   ========

Returns all the mail in the user's mailbox. 

Reads mail from the **new** and **cur** directories.
Marks all new mail as **read** and moves them to **cur** directory.

##### Sample Request

```json
{
	"world" : 0,
	"function" : "get_all_mail",
	"data" : {
		"token" : "TOKEN"
	}
}
```

##### Sample Responses

```json
{
	"status" : 0,
	"message" : "successfully recieved all mail",
	"data" : [ list of all mail ]
}
```

## ========   get new mail   ========

Returns all the new, unread mail in the user's **new** mailbox.

All mail returned this way is marked as **read** on the server side, regardless of whether or not the client has actually read the mail.
Additionally moves all new mail to the **cur** directory.

##### Sample Request

```json
{
	"world" : 0,
	"function" : "get_new_mail",
	"data" : {
		"token" : "TOKEN"
	}
}
```

##### Sample Responses

```json
{
	"status" : 0,
	"message" : "successfully recieved all new mail",
	"data" : [ list of all mail ]
}
```

## ========   delete mail   ========

Deletes the user's selected mail from the server.

##### Sample Request

```json
{
	"world" : 0,
	"function" : "delete_mail",
	"data" : {
		"token" : "TOKEN",
		"mail" : mail
	}
}
```

##### Sample Responses

```json
{
	"status" : 0,
	"message" : "success",
}
```

# Private


## ========   send mail   ========

Sends mail to the specified user.

Send a POST request with the following parameters to the mail server at the **/send\_mail** endpoint.

At minimum, every request must have **world** and **uid\_to**.
However, the message created by such a simple request will not be very interesting.
The last parameter, **kwargs**, functions as a simple key-value store to create more robust messages.

The **from**, **subject**, **body**, and **type** arguments should be included if possible in every message.

Current valid types of messages:
- **simple** - A simple message containing only text
- **gift**   - A message containing text and a gift attachment

If the type of message is **gift**, additional arguments are required (inside kwargs)
```json
"items" : a str containing comma separated items - str,
"quantities" : a string containing comma separated quantities - str
```

Example
```json
"items" : "skill_scroll_10,coin",
"quantities" : "4,300"
```

##### Sample POST

```json
{
	"world" : int or str,
	"uid_to": the unique_id of the recipient - str,
	"kwargs":
	{
		"from" : the name of the sender - str,
		"subject" : the subject line of the message - str,
		"body" : the main body of the message - str,
		"type" : the type of the message - str
	}
}
```

Example
```json
{
	"world" : "0",
	"uid_to": "4",
	"kwargs":
	{
		"from" : "",
		"subject" : "You have a gift!",
		"body" : "Congradulations! You have a gift waiting to be retrieved!",
		"type" : "gift",
		"items": "skill_scroll_10, coin",
		"quantities" : "4, 300"
	}
}
```

##### Sample Responses

```json
{
	"status" : 0,
	"message" : "success",
	"data" : {}
}
```


## ========   broadcast mail   ========

Sends a piece of mail to all users.
This could take a while.

##### Sample Request

```json
{
	"world" : 0,
	"function" : "broadcast_mail",
	"data" : {
		"mail" : mail
	}
}
```

##### Sample Responses

```json
{
	"status" : 0,
	"message" : "success",
	"data" : {}
}
```
