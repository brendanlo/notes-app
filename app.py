"""Flask app for Notes"""

from flask import Flask, render_template, redirect, session, flash

from models import db, connect_db, User, Note
from forms import RegisterForm, LoginForm, CSRFProtectForm, AddNoteForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.get('/')
def root():
    """Renders home page"""

    return redirect('/register')


@app.route('/register', methods=["GET", "POST"])
def show_register_form():
    """Shows registration form"""

    form = RegisterForm()

    if form.validate_on_submit():
        # all_users = User.query.all()
        # if email is in (all_users.email)

        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)

        db.session.add(user)
        db.session.commit()

        # add user to flask session

        return redirect('/login')  # user/username

    else:
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
            form.username.errors = ["Username/password is incorrect"]

    return render_template('login.html', form=form)


@app.get('/users/<username>')
def show_user_details(username):
    """Shows user detail page"""

    user = User.query.get_or_404(username)
    form = CSRFProtectForm()

    # check username in the session matches endpoint
    if user.username != session['username']:
        flash("You are not authorized. Go away.")
        return redirect('/')

    else:
        return render_template('user_details.html', user=user, form=form)


@app.post('/logout')
def logout_user():
    """Logging out the current user, redirects to root"""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop('username', None)

    return redirect('/')


@app.get('/secret')
def show_secret_page():
    """Shows secret page if user is authorized"""

    # do we need to call form for every page bc the logout button needs form.hidden_tag()
    form = CSRFProtectForm()

    if 'username' not in session:
        flash("You are not authorized. Go away.")
        return redirect('/')
    else:
        return render_template('secret.html', form=form)


@app.post('/users/<username>/delete')
def delete_user(username):
    """Deletes user"""

    user = User.query.get_or_404(username)
    form = CSRFProtectForm()

    #Need to add validate_on_submit
    
    if user.username != session['username']:
        flash("You are not authorized. Go away.")
        return redirect('/')
    else:
        Note.query.filter_by(owner=username).delete()
        User.query.filter_by(username=username).delete()
        db.session.commit()
        session.pop('username', None)
        flash("User deleted")
        return redirect('/')

@app.route('/users/<username>/notes/add', methods=["GET", "POST"])
def add_note(username):
    """Shows add note form"""

    user = User.query.get_or_404(username)
    form = AddNoteForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        owner = username

        note = Note(title=title, content=content, owner=owner)

        db.session.add(note)
        db.session.commit()

        return redirect(f'/users/{username}')

    else:
        return render_template('add_note.html', form=form)

