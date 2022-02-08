from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


class User(db.Model):
    """User model"""

    __tablename__ = 'users'

    username = db.Column(
        db.String(20),
        primary_key=True,
        nullable=False,
    )

    password = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    first_name = db.Column(
        db.String(30),
        nullable=False
    )

    last_name = db.Column(
        db.String(30),
        nullable=False
    )

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user with hashed password and returns user"""

        hashed = bcrypt.generate_password_hash(pwd).decode('utf8')

        return cls(
            username=username,
            password=hashed,
            email=email,
            first_name=first_name,
            last_name=last_name
            )

    @classmethod
    def authenticate(cls, username, password):
        """Validate that the user exists and password is correct
        
        Return user if valid; else return False
        """

        user = cls.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False