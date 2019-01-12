from flask_restful import Api
from app.resources.products import ProductsResource, ProductResource
from app.resources.prices import PricesResource
from app.resources.shops import ShopsResource,ShopResource
from app.resources.auth import LoginResource, LogoutResource
from webargs.flaskparser import parser, abort


@parser.error_handler
def handle_request_parsing_error(err, *_unused):
    abort(400, errors=err.messages)


api = Api(prefix='/observatory/api')
api.add_resource(ProductsResource, '/products')
api.add_resource(ProductResource, '/products/<int:prod_id>')
api.add_resource(PricesResource, '/prices')
api.add_resource(ShopsResource, '/shops')
api.add_resource(ShopResource, '/shops/<int:shop_id>')
api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')