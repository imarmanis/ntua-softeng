import pytest
from app import create_app
from app.models import db, User


@pytest.fixture(scope="class", params=['postgresql+psycopg2://root:root@localhost:5432/testing'], autouse=True)
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


@pytest.fixture(scope="class")
def root():
    db.session.add(User(username='root', password='root'))
    db.session.commit()
