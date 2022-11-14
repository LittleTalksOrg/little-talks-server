# Little Talks - Server

Simple server for [Little Talks](https://littletalks.org) using [Flask Framework](https://flask.palletsprojects.com) and [SQLite3](https://www.sqlite.org/index.html). It´s an experimental chat server based on a latitude/longitude location.

## Endpoints
We just receive a `POST` request on root and response the last 25 msgs in that location.

### Request Params:
- msg: message you want to send. (blank to send nothing)
- nickname: a nickname of your user
- lat: latitude you want to talk
- lng: longitude you want to talk

### Request Response:
- Shell formatted text with 25 last message;

## Execution

```Shell
flask run
```