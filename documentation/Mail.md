# Mail

Mail is responsible for handling all requests pertaining to the user's mailbox.
A user's mailbox can contain announcements to all the players, friend requests, and gift items from other players.
The mailbox is different per world.

Internally, the mailbox stores mail on disk in the standard email Maildir format.
The Maildir format does not use a database to manage files, rather it uses a directory structure to organize mail.


See the General Server documentation for more information on request and response format.


# General API Documentation

**NOTE - Error codes have yet to be formalized**

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

Depending on the type of message, you can expect to find these additional items in **data**:
- **simple**:
	- No additional items.
- **gift**:
	- nonce - a one time use code to redeem the gift
- **friend\_request**:
	- nonce - a one time use code to confirm friend request
	- sender - the game name of the user who sent the request





# Public

## ========   get new mail   ========

Returns all the new mail in the user's **new** mailbox.

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


## ========   get all mail   ========

Returns all the mail in the user's mailbox. 

Reads mail from the **new** and **cur** directories.
Moves all mail in the **new** directory to the **cur** directory.

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


## ========   delete all mail   ========

Deletes all of the read mail in the user's mailbox.
Unread mail in the **new** directory is preserved.

##### Sample Request

```json
{
	"world" : 0,
	"function" : "delete_all_mail",
	"data" : {
		"token" : "TOKEN"
	}
}
```

##### Sample Responses

```json
{
	"status" : 0,
	"message" : "successfully deleted all mail",
	"data" : [ list of all mail ]
}
```


# Private


## ========   send mail   ========

Sends mail to the specified user.

Send a POST request with the following parameters to the mail server at the **/send\_mail** endpoint.

**NOTE** - When making requests, be sure to send your POST data as a **json**.

At minimum, every request must have **world** and **uid\_to**.
However, the message created by such a simple request will not be very interesting.
The last parameter, **kwargs**, functions as a simple key-value store to create more robust messages.

The **from**, **subject**, **body**, and **type** arguments should be included if possible in every message.

Current valid types of messages:
- **simple** - A simple message containing only text
- **gift**   - A message containing a gift attachment
- **friend\_request** - A message containing a friend request

If the type of message is **gift**, additional arguments are required (inside kwargs):
```json
"items" : a str containing comma separated items - str,
"quantities" : a string containing comma separated quantities - str
```

Example
```json
"items" : "skill_scroll_10,coin",
"quantities" : "4,300"
```

If the type of message is **friend\_request**, additional arguments are required (inside kwargs):
```json
"sender" : the game name of the friend request sender,
"uid_sender" : the unique_id of the sender
```

##### Sample POST (json format)

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

Example - sending a gift message to a user containing 4 skill\_scroll\_10, and 300 coins.

(Using requests library for example. Please use async library in production code)
```python
data = {'world':'0','uid_to':'4','kwargs':{'from':'server','subject':'You have a gift!','body':'Your gift is waiting','type':'gift','items':'skill_scroll_10,coin', 'quantities':'4,300'}}
requests.post('MAILSERVERURL/send_mail', json = data)
```

data:
```json
{
	"world" : "0",
	"uid_to": "4",
	"kwargs":
	{
		"from" : "server",
		"subject" : "You have a gift!",
		"body" : "Your gift is waiting",
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

## ========   delete mail   ========

Deletes the message with the associated nonce from the user's mailbox.

After a user redeems something using the message **nonce**, that message should be deleted from their mailbox.
This operation, however, is not automatic.
It is the responsibility of the redeem function author to call this function to delete that message.
Has no effect if a message with the provided nonce does not exist.

Send a POST request with the following parameters to the mail server at the **/delete\_mail** endpoint.

##### Sample POST

```json
{
	"world" : 0,
	"unique_id" : str,
	"nonce" : str
}
```

(Using requests library for example. Please use async library in production code)
```python
requests.post('MAILSERVERURL/delete_mail', data = {'world':0, 'unique_id':'4', 'nonce':'23423'})
```

##### Sample Responses

```json
{
	"status" : 0,
	"message" : "success"
}
```

## ========   broadcast mail   ========

Sends a piece of mail to all users specified.

The **mail** parameter follows the same formatting as the **kwargs** section in the **send\_mail** function.

This could take a while.

##### Sample POST (json format)

```json
{
	"world" : 0,
	"users" : [uid1, uid2, ..., uidn],
	"mail":
	{
		"from" : the name of the sender - str,
		"subject" : the subject line of the message - str,
		"body" : the main body of the message - str,
		"type" : the type of the message - str
	}
}
```

(Using requests library for example. Please use async library in production code)
```python
data = {
		'world' : '0',
		'users' : ['1', '2', '3', '4', '5'],
		'mail' : 
			{
			'from' : 'server',
			'subject' : 'Server Announcement',
			'body' : 'Servers will undergo standard maintenance from 14:00 - 14:30.',
			'type' : 'simple'
			}
		}

requests.post('MAILSERVERURL/broadcast_mail', json = data)
```

##### Sample Responses

```json
{
	"status" : 0,
	"message" : "success",
	"data" : {}
}
```
