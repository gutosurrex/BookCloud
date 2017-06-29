import pytest

from application import create_app, db as the_db

the_app = create_app(dict(
    TESTING=True,  # Propagate exceptions
    LOGIN_DISABLED=False,  # Enable @register_required
    MAIL_SUPPRESS_SEND=True,  # Disable Flask-Mail send
    SERVER_NAME='localhost',  # Enable url_for() without request context
    SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',  # In-memory SQLite DB
    WTF_CSRF_ENABLED=False  # Disable CSRF form validation
))

def find_or_create_user(name, email, password):
    """ Find existing user or create new user """
    from application import User
    user = User.query.filter(User.username == name).first()
    if not user:
        user = User(username=name,
                    password=the_app.user_manager.hash_password(password),
                    email=email,
                    active=True)
        the_db.session.add(user)
    return user

def create_users():
    """ Create users when app starts """

    # Create all tables
    the_db.create_all()

    # Add users
    user = find_or_create_user(u'foo', 'foo@example.com', 'Foo123')
    user = find_or_create_user(u'bar', 'bar@example.com', 'Bar123')
    user = find_or_create_user(u'bla', 'bla@example.com', 'Bla123')

    # Save to DB
    the_db.session.commit()

create_users()

@pytest.fixture(scope='session')
def app():
    return the_app


@pytest.fixture(scope='session')
def db():
    """
    Initializes and returns a SQLAlchemy DB object
    """
    return the_db
