from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from myseriallist.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=18)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    confirm_password = StringField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    @staticmethod
    def validate_username(username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exists")

    @staticmethod
    def validate_email(email):
        email = User.query.filter_by(username=email.data).first()
        if email:
            raise ValidationError("Email already exists")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=18)])
    password = StringField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

    submit = SubmitField('Log In')


class SerialForm(FlaskForm):
    watch_status = SelectField("Watch Status", choices=[("plan", "Plan to Watch"), ("hold", "On Hold"),
                                                        ("watch", "Watching"), ("drop", "Dropped")])
    add_to_list = SubmitField('Add to List')
    update = SubmitField("Update")
    series_watched = IntegerField('Series Watched')


class AddSerialForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    series_number = IntegerField('Series number', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=0, max=1000)])
    submit = SubmitField('Add')
