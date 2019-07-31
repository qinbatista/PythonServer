# Mailbox Manager

Mailbox Manager is responsible for handling all requests pertaining to the user's mailbox.
A user's mailbox can contain announcements to all the players, friend requests, and gift items from other players.
The mailbox is different per world.

Internally, the mailbox manager stores mail on disk in the standard email Maildir format.
The Maildir format does not use a database to manage files, rather it uses a directory structure to organize mail.


See the General Server documentation for more information on request and response format.


## API Documentation and Sample Requests


To be described later

Standard mail json format.
All mail returned by the server to the client will follow this format.

**callback** and **args** keys are only present if **has\_attachment** is **true**.

```json
{
	"subject" : str,
	"time_recieved" : str,
	"body" : str,
	"has_attachment" : boolean,
	"callback" : str,
	"args" : {
		"key" : "value"
	}
}
```




# Public

## ========   get all mail   ========

Returns all the mail in the user's mailbox. 

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

Returns all the new, unread mail in the user's mailbox.

All mail returned this way is marked as 'Read' on the server side, regardless of whether or not the client has actually read the mail.

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

# Private


## ========   send mail   ========

Sends the mail to the specified user.

##### Sample Request

```json
{
	"world" : 0,
	"function" : "get_all_mail",
	"data" : {
		"sender" : "unique_id",
		"recipient" : "unique_id",
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
