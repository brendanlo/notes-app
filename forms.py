from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length
from models import User

"""Forms for Notes application"""


class RegisterForm(FlaskForm):
    """Form for registering a new user"""

    username = StringField("Username",
                           validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password",
                             validators=[InputRequired(), Length(max=100)])
    email = StringField("E-Email Address",
                        validators=[InputRequired(), Email()])  # unique?
    first_name = StringField("First Name",
                             validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name",
                            validators=[InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    """Form for logging a user in"""

    username = StringField("Username",
                           validators=[InputRequired()])
    password = PasswordField("Password",
                             validators=[InputRequired()])


class AddNoteForm(FlaskForm):
    """Form for adding note"""

    title = StringField("Title",
                        validators=[InputRequired(), Length(max=100)])

    content = StringField("Content",
                        validators=[InputRequired()])


class CSRFProtectForm(FlaskForm):
    """Emtpy form just for CSRF protection"""
