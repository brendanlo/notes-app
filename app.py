"""Flask app for Notes"""

from flask import Flask, render_template, redirect, session, flash

from models import db, connect_db, User
from forms import RegisterForm, LoginForm

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


@app.route('/register', methods=["GET", "POST"])
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

        return redirect('/secret')

    else:
        form.errors = ["Value is invalid"]

    return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def show_login_form():
    """Shows login form"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username

            return redirect(f'/users/{username}')

        else:
            form.errors = ["Username/password is incorrect"]

    return render_template('login.html', form=form)


@app.get('/users/<username>')
def show_user_details(username):
    """Shows user detail page"""

    user = User.query.get_or_404(username)

    if "username" not in session:
        flash("You are not authorized. Go away.")
        return redirect('/')

    else:
        return render_template(f'/users/{username}', user=user)

# @app.get('/secret')
# def show_secret_page():
#     """Shows secret page if user is authorized"""

#     if "username" not in session:
#         flash("You are not authorized. Go away.")
#         return redirect('/')

#     else:
#         return render_template('secret.html')
