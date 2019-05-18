# myseriallist

## Start
To start on local host:
```
$ python3 run.py
```
## Requirements
__I've used couple of flask extensions:__
  * [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) (support for SQLAlchemy) : 
  * [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) (integration of Flask and WTForms) : 
  * [Flask-Login](https://flask-login.readthedocs.io/en/latest/) (user session management for Flask) : 
```
$ pip install -r requirements.txt
```
## About
__Right now there are several features:__
  * You can _register/login/logout_
  * If you are _logged in,_ you can _add_ a serial to the database
  * If you are _logged in_, you can _add_ an _existing_ serial to your _serial-list_
  * You can set a _watch status_ for a serial in _your list_
  * You can set how many _series_ of a serial in _your list_ you have watched
