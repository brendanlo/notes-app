"""Flask app for Notes"""

from flask import Flask, request, render_template, redirect

from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.get('/')
def root():
    """Renders home page"""

    return redirect('/register')


@app.router('/register', methods=["GET", "POST"])
def show_register_form():
    """Shows registration form"""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)

        db.session.add(user)
        db.session.commit()

    else:
        form.username.errors = ["Value is invalid"]

    return render_template('register.html', form=form)