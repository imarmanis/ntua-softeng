import pytest
from app import create_app
from app.models import db, User
from tests import data


@pytest.fixture(scope="module", params=['postgresql+psycopg2://root:root@localhost:5432/testing'], autouse=True)
def client(request):
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = request.param
    app.config['SQLALCHEMY_ECHO'] = False
    app.testing = True
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="module")
def user1():
    user = User(**data.users[0])
    db.session.add(user)
    db.session.commit()
    yield data.users[0]
    db.session.delete(user)
    db.session.commit()


@pytest.fixture(scope="module")
def root():
    user = User(**data.root, is_admin=True)
    db.session.add(user)
    db.session.commit()
    yield user
    db.session.delete(user)
    db.session.commit()


@pytest.fixture(scope="module")
def user1_token():
    return User.query.filter(User.username == data.users[0]['username']).first().token
