from myseriallist import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Connection(db.Model):
    connection_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    serial_id = db.Column(db.Integer, nullable=False)
    series_watched = db.Column('series_watched', db.Integer, default=0)
    watch_status = db.Column(db.String(100), default='plan_to_watch')


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


    def get_id(self):
           return (self.user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Serial(db.Model):
    serial_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    series_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)


