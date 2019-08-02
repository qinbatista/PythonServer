# Token Server

The Token Server acts as a single central authority on the network for issuing and validating tokens and nonces.
**All methods of the token server are private only and should never be exposed to public.**

See the General Server documentation for more information on request and response format.

# General API Documentation

**NOTE - Error codes have yet to be formalized**

# Private

## ========   redeem nonce   ========

Redeem the nonce if valid.
A nonce can only be used one time, subsequent calls using the same nonce will always fail.

**NOTE** Requests made to this function must be formatted as **json**.

Current valid types, and expected results in **data**:
- **gift**
	- **items** : a string containing comma separated item names
	- **quantities** : a string containing comma separated quantities for the respective items
- **friend\_request**
	- **uid\_sender** : the unique\_id of the friend request sender


##### Sample POST

```json
{
	"type" : str,
	"nonce": str
}
```

##### Sample Responses

```json
{
	"status" : 0,
	"message" : "successfully redeemed",
	"data" :
	{
		optional key-value pairs
	}
}
```
