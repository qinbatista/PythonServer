# SkillManager

The SkillManager is responsible for handling requests pertaining to upgrading and querying skills.

See the General Server documentation for more information on request format.


## API Documentation and Sample Requests

The following sections each describe supported function / API calls from the client to the server as well as their accompanying response. Internal Manager HTTP API calls are not described here.


Any function call that is not formatted correctly will receive the following response:
```json
{
	"status" : "10",
	"message": "invalid message format",
	"data" : {}
}
```

Any function call that requires a valid token and does not supply one will receive the following response:
```json
{
	"status" : "11",
	"message": "authorization required",
	"data" : {
				"bad_token" : "VALUE OF BAD TOKEN"
			 }
}
```



### skill\_level\_up

Levels up a skill. If the skill level is 0, the user cannot level up that skill. In order to level up that skill, you need to use a scroll. The scroll gives a probability that the skill will level up.

Status codes and meaning:

- 0 - Success
- 1 - User does not have that skill
- 2 - User does not have enough scrolls
- 9 - Skill already at max level

The UPGRADE\_SUCCESS value in the server's response can be either 0 or 1 depending upon whether or not the skill actually leveled up. A failure here does not mean a failed API call - it means that the scroll skill did not yield a level up. Different levels of scroll skills have different success rates.

##### Sample Request
```json
{
	"function" : "skill_level_up",
	"data" : {
				"token" : "valid token here",
				"skill_id" : "skill id here",
				"scroll_id" : "scroll id here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"skill1": [skill_id, result of skill level],
				"item1" : [scroll_id, resulting scroll quantity],
				"upgrade" : "UPGRADE_SUCCESS"
			 }
}
```



### get\_all\_skill\_level

Returns all the current skill levels.

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"function" : "get_all_skill_level"
	"data" : {
				"token" : "valid token here",
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"skill1": [skill_name, skill_value],
				.
				.
				.
				"skillN" : [skill_name, skill_value]
			 }
}
```




### get\_skill

Returns the requested skill level.

Status codes and meaning:

- 0 - Success
- 1 - Invalid skill name


##### Sample Request
```json
{
	"function" : "get_skill"
	"data" : {
				"token" : "valid token here",
				"skill_id"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"skill1": [skill_name, skill_value],
				.
				.
				.
				"skillN" : [skill_name, skill_value]
			 }
}
```



### random\_gift\_skill

Gives a random chance to unlock a new skill if it doesn't already exist. If it does exist, the user gets a free skill scroll.

Status codes and meaning:

- 0 - Success
- 1 - You already have that skill, you got a new scroll for free!


##### Sample Request
```json
{
	"function" : "random_gift_skill"
	"data" : {
				"token" : "valid token here",
			 }
}
```

##### Sample Responses
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"skill1": [skill_id, 1]
			 }
}
```

```json
{
	"status" : "1",
	"message": "You already have that skill, you get a new scroll for free1",
	"data" : {
				"item1": [scroll_skill_id, scroll_skill_quantity]
			 }
}
```
