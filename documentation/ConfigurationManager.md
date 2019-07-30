# ConfigurationManager

The ConfigurationManager provides a centralized service for handling requests pertaining to the server and client configurations.
The configuration manager periodically reads the most current version of the configuration files, always keeping an up-to-date version of the configuration.


See the General Server documentation for more information on request and response format.


## API Documentation and Sample Requests

All API calls to the ConfigurationManager are to be made as simple GET requests, with no parameters.

No authentication is needed.



---



## ========   get\_game\_manager\_config   ========

Provides the configurations needed by the game manager.

Source configuration files are in .json format.

##### Sample Responses

```json
{
	"reward_list" : [ ... ],
	"lottery" : { ... },
	"weapon" : { ... }
}
```



## ========   get\_level\_enemy\_layouts\_config   ========

Provides the configuration for the enemy layouts for each level.

Source configuration files are in .json format.


##### Sample Response

```json
{
	"enemy_layouts" : [ ... ]
}
```



## ========   get\_monster\_config   ========

Provides the configuration for the monster stats.

Source configuration files are in .json format.


##### Sample Response

```json
{
	"MONSTER_NAME" : {
		"STAT_NAME" : VALUE
	}
}
```

## ========   get\_stage\_reward\_config   ========


Provides the configuration for the stage rewards.

Source configuration files are in .json format.


##### Sample Response

```json
{
	"STAGE_NUMBER" : {
		"ITEM_NAME" : VALUE
	}
}
```

## ========   get\_hang\_reward\_config   ========

Provides the configuration for the hang rewards.

Source configuration files are in .json format.


##### Sample Response

```json
{
	"STAGE_NUMBER" : {
		"ITEM_NAME" : VALUE
	}
}
```


## ========   get\_mysql\_data\_config   ========

Provides the configuration for the mysql server table layout.

Source configuration files are in .json format.


##### Sample Response

```json
{
	"TABLE_NAME" : [ COLUMNS ],
	"TABLE_NAME" : [ COLUMNS ]
}
```
