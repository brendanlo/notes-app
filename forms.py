from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired

"""Forms for Notes application"""

class RegisterForm(FlaskForm):
    """Form for registering a new user"""

    username = StringField("Username",
                validators=InputRequired())
    password = StringField("Password",
                validators=InputRequired())
    email = StringField("E-Email Address",
                validators=InputRequired())
    first_name = StringField("First Name",
                validators=InputRequired())
    last_name = StringField("Last Name",
                validators=InputRequired())

