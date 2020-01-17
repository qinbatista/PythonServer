# 服务器部署

这个文档的目的就是描述搭建Lukseun服务器的基础步骤。

This guide assumes some basic familiarity with the **linux** system, as well as the **command line**.
The most important skill is being able to research solutions to problems.

**Table of Contents**

* [Database](#Database)
  * [Local Testing Database](#Local-Testing-Database)
  * [Production Database](#Production-Database)
* [Redis](#Redis)
  * [Local Testing Redis](#Local-Testing-Redis)
  * [Production Redis](#Production-Redis)
* [Nats](#Nats)
  * [Local Testing Nats](#Local-Testing-Nats)
  * [Production Nats](#Production-Nats)
* [Kubernetes](#Kubernetes)
* [Docker](#Docker)

## Database

We use MySQL for our database backend.
Compatible open-sourced alternatives such as MariaDB are also acceptable.

The database instance should not be hosted within a Kubernetes cluster.
Instead, it should be hosted on a dedicated machine(s).

### Local Testing Database

For testing and development purposes, it is useful to create a database on the local network.

This guide will assume a new up-to-date Debian installation, however other linux distributions should be similar.

Debian should already have the MariaDB package in the respositories.

To install, run `apt install mariadb-server`.

You can check if the server is running with `systemctl status mariadb`.
If the server is not already running, you can restart it with `systemctl restart mariadb`.

To create a secured system, you can run `mysql_secure_installation`.
After the secured installation completes, the priviledge tables will be reloaded.

If you can not connect to the database from remote systems, you might have to modify the priviledge table.
Connect to the database directly `mysql -u root -p`.
Issue the following command to allow remote access to the root account from all computers (not secure for production): `GRANT ALL PRIVILEDGES ON *.* TO 'root'@'%' IDENTIFIED BY 'PASSWORD';` replacing `PASSWORD` with the root password.
Then issue `FLUSH PRIVILEGES;` to reload the configuration.

### Production Database

For production, you should use a managed database service.
An example of such is Aliyun's RDS service.

You can use the web GUI to create a new managed database instance.
You can create user names and passwords, as well as perform other database management using the web GUI.


## Redis

### Local Testing Redis

The easiest way to run Redis locally is via Docker.

If you have Docker installed, you can run `docker run -d --name redis -p 6379:6379 redis:latest`.

### Production Redis

Depending upon how heavily the Redis usage is, you might consider using a fully hosted Redis solution.

In other cases, it is possible to run Redis within a Kubernetes cluster.

## Nats

### Local Testing Nats

The easiest way to run Nats locally is via Docker.

If you have Docker installed, you can run `docker run -d --name nats -p 4222:4222 nats:latest`.

### Production Nats

It is fine to run Nats within a Kubernetes cluster, but it is recommended to run more than one instance.

In that case, you will need to ensure Nats swarm mode has been configured properly.


## Kubernetes

It is generally quite difficult to test Kubernetes locally.
However, the `minikube` package available on most linux systems attempts to solve this problem.

Most of the time, it is sufficient to test locally using only Docker.

An example of that would be the following:

* Run a docker container for each service we have. (Make sure to publish the ports using the *-p* option)
* You can test by pointing the client to the ip address of the Docker host machine.
* After confirming everything is working as intended, you can deploy things on Kubernetes.

In general, you would want to create a Kubernetes Deployment for each Docker image you have running.
Then, you would generally want to create a Kubernetes Service for each Deployment you made.
Containers within the cluster can use the Service IP assigned to each Service to access other containers in the cluster.

When using Kubernetes in production, most configuration can be made using an online GUI.

It is highly recommended to complete the tutorial found here: [Interactive Tutorial](https://kubernetes.io/docs/tutorials/kubernetes-basics/)

## Docker

In order to run Docker containers, a host has to have the Docker service installed and running.

This guide will assume a new up-to-date Debian installation, however other linux distributions should be similar.

1. Remove all old instances of Docker `apt-get remove docker docker-engine docker.io containerd runc`
2. Install packages required to use HTTPS `apt-get install apt-transport-https ca-certificates curl gnupg2 software-properties-common`
3. Add official Docker GPG key `curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -`
4. Add Docker repository `add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"`
5. Update repository list `apt-get update`
6. Install latest version of Docker `apt-get install docker-ce docker-ce-cli containerd.io`
7. Ensure Docker is running by trying `docker run hello-world`