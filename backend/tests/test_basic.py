import pytest
from datetime import date
from app.models import db, Product, Shop, User
from tests import url_for, auth_header
from tests import data
from werkzeug.datastructures import MultiDict


@pytest.mark.usefixtures("user1", "root")
class TestAuth(object):
    def test_login(self, client):
        rv = client.post(url_for('/login'))
        assert rv.status_code == 400

        rv = client.post(url_for('/login'), data=data.user1)
        assert rv.status_code == 200
        assert rv.json['token'] == User.query.filter(User.username == data.user1['username']).first().token

    def test_logout(self, client):
        token = User.query.filter(User.username == data.user1['username']).first().token

        rv = client.post(url_for('/logout'))
        assert rv.status_code == 403

        rv = client.post(url_for('/logout'), headers=auth_header(token))

        assert rv.status_code == 200
        assert not User.query.filter(User.username == data.user1['username']).first().token
        assert rv.json['message'] == "OK"
