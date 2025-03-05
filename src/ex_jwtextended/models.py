from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from jwtexample import db, jwt


class User(db.Model):
    """User model for use with login"""
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)

    def __init__(self, **kwargs):
        """Create a new User object hashing the plain text password."""
        super().__init__(**kwargs)
        password = kwargs["password"]
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Checks the text matches the hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        clsname = self.__class__.__name__
        return f"{clsname}: <{self.id}, {self.username}>"


# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()
