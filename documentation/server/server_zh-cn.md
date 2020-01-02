# 服务器架构

此文档的目的用于描述Lukseun Server System的架构和操作方法，文档会尽可能包含所有关于Kubernetes的管理与代码编写。

![](assets/overview.png)

**目录**

* [介绍](#介绍)
* [服务器快速入门](#服务器快速入门)
* [技术点](#技术点)
* [通用代码入门](#通用代码入门)
* [服务器模块](#服务器模块)
	* [Auth](#Auth)
	* [Config](#Config)
	* [Edge](#Edge)
	* [Gate](#Gate)
	* [Mail](#Mail)
	* [Worker](#Worker)
		* [worker.py](#workerpy)
		* [message_handler.py](#message_handlerpy)
		* [module](#module)
* [Docker](#Docker)
* [Kubernetes](#Kubernetes)



## 介绍

服务器设计的理念遵循**微型**高度可弹性伸缩结构。

每一个微型服务器初始为无状态，服务器会根据情况进行自动扩张，全程不需要做配置修改。

另外，每一个微型服务器都只服务一个项目。

如果一个微形服务器的功能是创建帐号或者验证登陆，他就不会做对方服务器的任务。

比如：目前我们有5个微形服务器处理游戏数据，只有其中一个会处理微型服务器会处理登陆任务。

这样的话我们可以更好分发和处理资源，就不会让所有的资源都在一台服务器上。

所以微型服务器的处理责任分发能力是最合适的。

为了实现我们的微形服务器结构，我们采用了**docker**和**kubernetes**技术。

**docker**可以给我们的服务器提供最方便的打包技术。

**Kubernetes**可以给我们的**docker**镜像提供配置器，部署和自动伸缩的功能

## 服务器快速入门

参考如上示例图。

我们现在假象我们的服务器没有聊天系统的消息处理。

在所有消息发送到服务器处理之前，所有的消息会发送到负载均衡服务器 `game.aliya.lukseun.com`。

负载均衡服务器随机发送到我们的gate服务器。

gata服务器在处理完部分账户操作之后，会把消息推送到message queue服务器。

message queue的的消息队列会一直等待相应的woker服务器来接收消息。

woker服务器会处理具体的逻辑然后返回结果，其中可能也会做数据库服务器操作和邮箱服务器操作。

在所有操作处理完毕之后，会返回给消息来源的gate服务器。

gate整理好收到的消息后，在返回给客户端。

整个流程大约在`10ms`左右。

现在让我们来假设整个流程，抛开时间因素，我现在是一个消息。

客户端会发送消息到`edge.aliya.lukseun.com`以加入聊天服务器。

在`edge.aliya.lukseun.com`的负载均衡的服务器会把消息分发到其中一个edge服务器结点。

之后会在客户端和服务器创立一个持续性的tcp连接，edge服务器不会在连接期间做任何改变。

消息流会自由的在客户端和edge服务器之间进行来往。

## 技术点

这里面有部分技术是我们文档没有提到的。

他们大部分都是标准化的技术而且官方提供非常专业的文档。

如下所示:

* Redis
* Nats
* MySQL

## 通用代码入门

责任分明和无差别区分思想是我们设计程序的主要思路。

每一个功能模块都有自己的目录

所有和此功能相关的文件都应该放在这个目录。

比如：代码，关联库和python安装库。

再次强调，不要把无关文件放入到模块的目录中。

另外在每个模块文件夹中，也必须要包含**Dockerfile**

当我们设计服务器的时候，我们首先考虑的是无差别性。

我们刚开始设计聊天系统的时候，每一个世界都有一个聊天系统。

如果这个聊天系统属于世界1就只能连接世界1的服务器。

这样的设计有几个问题。

首先，我们需要给每一个世界创建一个聊天服务器，不管是否有人在这个聊天服务器。

其次，如果一个聊天服务器特别繁忙，我们没有办法让其他服务器来帮忙分流。

这样的设计就叫无差别性。

所有的代码都有特定的地方填写参数来配置不同的功能。   

## 服务器模块

如下每一项介绍都关联对应的微型服务器。



### Auth

反馈登陆的合法性和验证结果。

注册和使用**nonces**。

API通过http post进行点对点传输。

服务器登陆的token遵循JWT标准。

他们会用命令行参数进行注册，注册码会用特别的加密值来进行标记。

token会包含用户的unique id。

nonces可以被注册，也可以被兑换。

因此nonces是唯一用来和服务器交互的关键

nonces和交互服务器标识都被caller函数定义。

nonces和交互服务器标识都在Redis中存储。

任何auth服务器都可以检索nonces关键字甚至他们并没有被Redis注册。

一旦nonces和交互服务器标识被检索，他们会立即从Redis中移除。



### Config

一个简单的http服务器，用于返回服务器所使用的配置文件信息。

他会周期性的从本地文件中读取配置文件，以用于确保使用最新的版本。



### Edge

这是一个简单的聊天服务器。

处理客户端连上不同世界的聊天服务器。

客户端提供nonce来连接聊天服务器，和登陆的token是一个道理。

Redis用nonce作为关键字来查询。

交互服务器标识包含了服务器的名字，世界和家族信息。

如果是合法的nonce，客户端可以直接聊天，否则会直接关闭连接。

聊天系统遵循simple protocol规则。

所有消息的前10位是命令集，结尾由`\r\n`。

期望的交互服务器标示在代码集中。

如果protocol没有遵循如上规则，服务器会立即中断连接。

Edge服务器利用Nats作为**公用**服务器来分发到每一个聊天服务器节点。

公共消息会发送到当前这个消息的世界所属频道：**chat.$WORLD.public** 

家族消息会发送到当前这个消息的家族所属频道**chat.$WORLD.family.$FN**频道，**FN**指代家族的名字。

因此，任何人连接了聊天平台以后，都可以从聊天同样接受消息。

这样的话就可以非常方便的加入所有聊天消息。

Edge服务器会让每一个客户端连接上对应的服务器。

一旦edge服务器接收到对应聊天频道的消息，他会把消息广播到所有连接上聊天服务器的频道。



### Gate

gate服务器是用来接收客户端的消息，并由指定的服务器来处理。

一旦接受到客户端发送过来的消息，消息会推送到message queue，然后等待消息返回。

当gate服务器开始运作的时候，他会创建一个用于gate交互的id。

不会存在两个gate拥有一个id。

gate服务器会从redis中获得缓存来获得ip地址和gate id。

gate服务器利用的Redis关键字为 **gates.id.$GID**,其中 **$GID** 是唯一识别码id。

gate服务器会周期性的发送消息到Redis，以表示这个gate id正在开放中。

gate服务器实际上同时会运行两个tcp连接。

第一个服务器是客户端服务器，其默认端口为8880。

客户端服务器工具会遵循如下逻辑。

当gate服务器接收到一个客户端的消息，他会生成一个unique id来跟踪整个消息流程。

gate服务器会保持一个字典用于保存消息id和客户端套接字的值。

gate服务器也会用Redis来关联消息id和gate的gate标示id。

客户端会把消息打包并附上消息id，然后推送到Nats消息队列。

在这之后，gate会一直等到消息返回。

当gate服务器收到消息回复会立即把消息推送给客户端，然后清理缓存。

gate服务器会在redis中删除带有消息id和客户端套接字的字典。

Redis进入之后会自动创建一个message和gate id并在10秒后自动删除。

gate服务器连接的第二个服务器是worker服务器，默认端口为8201。

worker服务器会把消息处理完毕之后返回给gate。

这个工作非常简单，等待发送给worker服务器的消息返回。

当一个woker返回给gate 的消息，必定包含message id和实际的返回内容。

这个消息会被识别然后发送到对于的客户端套接字。

这个消息会直接发送给客户端。

然后关闭这个套接字。



### Mail

负责创建和检索所有的邮件。

邮箱系统是游戏的一个核心功能。

目前主要用作于家族，朋友和礼物。

邮箱系统的功能只外放一个简单的http post请求。

邮箱会存储到本地，遵循标准**Maildir**格式。

每一个邮件实际上就是一个独立的文件。

每一个世界都有一个单独的文件夹。

在每一个世界文件夹中，每一个文件夹也包含一个unique_id。

在每一个unique文件夹中，也会自动创建如下文件夹(cur, new, tmp)。

这些特别命名的文件夹就是邮箱的关键字。

每一个独立的邮箱都有这三个文件。

当一个邮件创立之后，邮箱服务器会分配一个unique id给每一个邮箱。

Maildir格式会让所有存储在邮箱的邮件都以ASCII的格式存储在磁盘中。

为了规避这个问题，我们要保证所有非ASCII码必须先转换为ASCII码在存储到磁盘中。

所有的值同样也会把所有ASCII码编码之后在发送。

在目前的环境中测试，游戏存储一切正常。

然而在实际操作中，邮箱应该存储在专门存放磁盘的地方，比如说NAS。

这样的话，一旦服务器出现问题，不会有任何邮件丢失。



### Worker

用于处理客户端的逻辑并且返回对应的结果给gate服务器。

worker由不同模块组成，每一个模块都有自己相应的说明文档。

#### worker.py

这个文件是woker服务器的切入点。

这是一整个处理NATs发送过来的消息框架，处理数据，返回数据等。

Mysql连接池会在这一层创建，与此同时，Redis和Nats也会在这一层创建。

Http的连接池也会在这时创建，以用于和其他服务器进行http交互。

worker会连接Nats服务器等待Nats服务器发送过来的消息。

当一个消息发到worker，消息也包含来自客户端的消息id。

woker会把消息id分离出来，然后提交消息到message_handler中处理。

一旦结果被获得之后，message id会用做在redis中查询gate id的关键字。

如果worker和gate的连接并未创立成功，一个新的连接就会被重新创立。

一旦消息处理完毕，就会把结果返回到正确的gate上。



#### message\_handler.py

专门用于解析预处理数据。

通过验证token（如果需要）是否合法来决定使用对于的功能。

如果token不能被验证，则返回失败结果给客户端。

所有无法被正常捕捉的错误都会返回**"programming error"**.

token验证通过之后，会找到对应的功能，在Function list中，功能列表是一个字典形式。

每一个功能的具体逻辑都在各自的模块中，模块的位置在`module`文件中。

#### module

这个文件夹包含所有代码模块的具体功能。

而且每一功能都自己独立的文件夹。

只有相关的文件才会放到同一个功能相同的文件夹中。

比如和家族相关的文件才会被写入到家族模块当中。

就如武器系统相关的文件就不能写入到家族模块中。

每一模块都用**函数式编程**思想去编写。

每一模块都不包含任何class类，直接用独立的方法去完成每一个功能。

这些所有的功能都会写进一个小型的

These functions should be broken up into smaller, logically coherent helper functions.
This helps improve readability.

Something to note is the extensive use of the `**kwargs` argument.
This argument contains many helpful tools the function might like to use.
These tools could be a database connection, redis connection, or an http client.
Additionally, configuration files can be found in the `**kwargs` argument.
These can be accessed via `kwargs['config'][ ... ]`.
You can reference the message\_handler's `resolve` function, which populates this `**kwargs` parameter, to find all the goodies it contains.
Ultimately, the kwargs parameter allows the programmer to have the convenience of always having access to commonly shared resources.
And eliminates the clutter of re-declaring network connections and config files everywhere.

Some unique modules declared are `common.py` and `enums.py`.
`common.py` contains commonly used functions.
Examples of these functions are database execution functions, and resolving uids to game names.
Do not put non-generic functions in this module.

`enums.py` defines a set of enums used by the entire server system.
These enums are also the same ones used by the client app.
The MySQL database makes extensive use of these enum values as composite keys.
This is because hashing and comparing int values is significantly faster than string values.
Use this module to define symbolic representations of items, roles, skills in the game.

## Docker

Our micro-service architecture demands an easy way to distribute and deploy our many servers.
With multiple servers, each with their own set of required third-party libraries, things can get out of hand quickly.
Fortunately, Docker provides us with an easy solution to all of that: Docker images.

You can think of a Docker image like a very simple Virtual Machine.
It provides an isolated environment for you to run your code in.
It contains all of the required third-party libraries needed to run your server, in addition to your code.
This image can then be run from any machine that can run Docker.

To create a Docker image, you need a Dockerfile.
A Dockerfile is like a recipe for the steps needed to create your perfect isolated environment.
You write instructions in the Dockerfile for how you would like to setup your "little virtual machine".
Extensive documentation can be found online for how to create a Dockerfile.

Once you have your Dockerfile created, you need to actually build the Docker image.
On linux, you can do that via the `docker build` command.
However, simplying building the docker image is not that helpful to us.
We want to both build the image, and publish it in a place that is easily accessible (you will see why later).

We will be using Aliyun's Container Registry service as a location to host our Docker images.
You can find information about this on Aliyun's website.
When building the images, you will need to tag them appropriately to be pushed to Aliyun's Registry.
For example, if I was building the Docker image for the gate service, I would issue a command like this:
`docker build -t registry.cn-hangzhou.aliyuncs.com/lukseun/gate:latest .`
to build the image.
Afterwards, I could issue:
`docker push registry.cn-hangzhou.aliyuncs.com/lukseun/gate:latest`
to push the built image to Aliyun's Registry.

Once the Docker images for our services have been built and pushed onto Aliyun's Registry, we need a method of deploying them.

## Kubernetes

Kubernetes, also know as K8S, is a service that will deploy and manage our micro-services.
It does this using the Docker images we have created and pushing to Aliyun.

There is extensive documentation online regarding the use and administration of kubernetes.
As such, this section will be left rather short, in favor of other documentation.
However, an excellent interactive tutorial can be found here: [Tutorial](https://kubernetes.io/docs/tutorials/kubernetes-basics/)

In general, we will want to create a Kubernetes Deployment for each micro-service.
For each of these deployments, we will want to create an internally load-balanced Kubernetes Service.
Each of our micro-services should reference the Kubernetes Service address if they need to communicate with another service.

Additionally, we will want to create externally load-balanced Kubernetes Services for the `edge` and `gate` deployments, as these are the only client facing servers.

We should assign public domain names (such as `edge.aliya.lukseun.com`) to each client facing load-balanced service.
The client app should use these domain names when connecting to our server.

