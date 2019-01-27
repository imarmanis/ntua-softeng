import pytest
from app.models import User
from tests import url_for, auth_header
from tests import data


@pytest.mark.usefixtures("user1", "root")
class TestBasic(object):
    def test_login(self, client, user1):
        rv = client.post(url_for('/login'))
        assert rv.status_code == 400

        rv = client.post(url_for('/login'), data=user1)
        assert rv.status_code == 200
        assert rv.json['token'] == User.query.filter(User.username == user1['username']).first().token

    @pytest.mark.parametrize("product_data", data.products)
    def test_add_product(self, client, product_data, user1_token):
        rv = client.post(
            url_for('/products'),
            headers=auth_header(user1_token),
            data=product_data
        )

        assert rv.status_code == 200
        assert product_data.items() <= rv.json.items()

    def test_list_products(self, client, user1_token):
        rv = client.get(
            url_for("/products?start=0&count=10&status=ACTIVE&sort=id%7CASC"),
            headers=auth_header(user1_token)
        )

        assert rv.status_code == 200
        assert rv.json['start'] == 0
        assert rv.json['count'] == 2
        assert rv.json['total'] == 2
        assert len(rv.json['products']) == 2
        for i, product in enumerate(data.products):
            assert product.items() <= rv.json['products'][i].items()

    def test_update_product(self, client, user1_token):
        prod1upd = data.products[0].copy()
        prod1upd.update({
            "name": 'bar-foo',
            "description": '4217a'
        })

        rv = client.put(
            url_for("/products/1"),
            headers=auth_header(user1_token),
            data=prod1upd
        )

        assert rv.status_code == 200
        assert prod1upd.items() <= rv.json.items()

    def test_get_product(self, client, user1_token):
        rv = client.get(
            url_for("/products/2"),
            headers=auth_header(user1_token)
        )

        assert rv.status_code == 200
        assert data.products[1].items() <= rv.json.items()

    def test_delete_product(self, client, user1_token):
        rv = client.delete(
            url_for("/products/2"),
            headers=auth_header(user1_token)
        )

        assert rv.status_code == 200
        assert rv.json['message'] == "OK"

        # TODO Shops

    def test_logout(self, client, user1):
        token = User.query.filter(User.username == user1['username']).first().token

        rv = client.post(url_for('/logout'))
        assert rv.status_code == 403

        rv = client.post(url_for('/logout'), headers=auth_header(token))

        assert rv.status_code == 200
        assert not User.query.filter(User.username == user1['username']).first().token
        assert rv.json['message'] == "OK"
