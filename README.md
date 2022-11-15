# Little Talks - Server

Simple server for [Little Talks](https://littletalks.org) using [Flask Framework](https://flask.palletsprojects.com) and [SQLite3](https://www.sqlite.org/index.html) or [Postgres](https://www.postgresql.org/). It´s an experimental chat server based on a latitude/longitude location.

## Endpoints
We just receive a `POST` request on root and response the last 25 msgs in that location.

### Request Params:
- msg: message you want to send. (blank to send nothing)
- nickname: a nickname of your user
- lat: latitude you want to talk
- lng: longitude you want to talk

### Request Response:
- Shell formatted text with 25 last message;

## Environment Vars
* `MSG_TABLE`: Table name for the messages;
* `DB`: `psql` for Postgres and `sqlite` for Sqlite; 

If you are using `Postgres`:
* `PS_DATABASE` = Database name;
* `PS_USER` = Database user;
* `PS_PASSWORD` = Database password;
* `PS_HOST` = Database host;
* `PS_PORT` = Database Port. In general 5432;

## Execution

```Shell
pip install -r requirements-dev.txt
pip install -r requirements.txt
flask run
```