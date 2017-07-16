# Hello Zookeeper

This is a `hello world`-like Project for 
[zookeeper](https://zookeeper.apache.org/),
[kazoo](https://github.com/python-zk/kazoo/) and 
[Flask](http://flask.pocoo.org/).

## Features

This project provides the next features:

- leader election;
- lease (service call a command only one time during the time period).

## Components

The project contains 4 services:

- zookeeper service;
- 3 nodes of application service with REST API on Flask.

One of the nodes of application services is a leader. 
Also, one of the nodes should print welcome message `"Welcome"`.

## Installation

I use [docker](https://www.docker.com/) and 
[docker-compose](https://docs.docker.com/compose/install/)
to develop and run this project.

```bash
$ make build
# docker-compose build
# Build a docker image for the application

$ make up
# docker-compose up -d app1 app2 app3
# Run containers in detached mode and expose ports 5001, 5002, 5003 
respectively.
$ curl localhost:5001
# {
#  "is_leader": false, 
#  "leader": "7e8d19d2ff984f889529dd6265997a34", 
#  "title": "Hello"
# }
$ docker-compose logs app1 app2 app3
# app2_1      | I'm a leader
# app2_1      | ::ffff:172.22.0.1 - - [2017-07-16 10:40:13] "GET / HTTP/1.1" 200 202 0.001051
# app3_1      | Welcome
# app3_1      | ::ffff:172.22.0.1 - - [2017-07-16 10:40:14] "GET / HTTP/1.1" 200 203 0.001507
# app1_1      | ::ffff:172.22.0.1 - - [2017-07-16 10:40:12] "GET / HTTP/1.1" 200 203 0.000895
```

## Local development

For local development without Docker I use 
[pipenv](https://github.com/kennethreitz/pipenv).

```bash
$ pipenv install
# Create a virtualenv if needed and install project dependencies
$ pipenv install --dev 
# Create a virtualenv if needed and install project dependencies and dev 
# dependencies
$ pipenv install {package_name}
# Install the project dependencies and save it in Pipfile
$ pipenv lock
# Update Pipfile.lock
```
