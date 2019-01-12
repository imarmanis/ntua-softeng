import itertools
from flask_restful import Resource
from flask import request
from webargs import fields
from webargs.flaskparser import use_args
from marshmallow import validate, ValidationError
from marshmallow.decorators import post_dump, pre_dump
from app.models import Shop,ShopTag, db, ma
from sqlalchemy import asc, desc
from app.resources.auth import requires_auth


SORT_CHOICE = list(map('|'.join, itertools.product(['name', 'id'],
                                                   ['ASC', 'DESC'])))
STATUS_CHOICE =['ALL','WITHDRAWN','ACTIVE']

ids_field = fields.List(fields.Int())
bad_request = '', 400
not_found = '', 404


class ShopTagSchema(ma.ModelSchema):
    @post_dump
    def flatten(self,data):
        return data['name']
    class Meta:
        model = ShopTag
        fields = ('name',)

class ShopSchema(ma.ModelSchema):
    tags = fields.Nested(ShopTagSchema, many=True)
    class Meta:
        model = Shop
        fields = ('id','name','address','lng','lat','tags','withdrawn')

shop_schema = ShopSchema()

class ShopsResource(Resource):
    @use_args({
        'start': fields.Int(missing=0, location='query',validate=validate.Range(min=0)),
        'count': fields.Int(missing=20, location='query',validate=validate.Range(min=0)),
        'sort': fields.Str(missing='id|ASC', location='query',
                           many=True, validate=validate.OneOf(SORT_CHOICE)),
        'status': fields.Str(missing='ACTIVE',location='query',validate=validate.OneOf(STATUS_CHOICE)),
	'format': fields.Str(missing='json', location='query',validate=validate.Equal('json'))
    })
    def get(self, args):
        query = Shop.query
        start = args['start']+1
        count = args['count']
        status = args['status']
        sort = {
            'id|ASC': Shop.id.asc(),
            'id|DESC': Shop.id.desc(),
            'name|ASC': Shop.name.asc(),
            'name|DESC': Shop.name.desc()
        }[args['sort']]
        if (status!='ALL'):
            query = query.filter_by(withdrawn=(status == 'WITHDRAWN'))
        query = query.order_by(sort)
        shops_page = query.paginate(start, count)
        shops = shop_schema.dump(shops_page.items,many=True).data
        return {
            'start': shops_page.page-1,
            'count': len(shops_page.items),
            'total': shops_page.total,
            'shops': shops
        }
    @requires_auth
    @use_args({
        'name': fields.Str(required=True, location='form'),
        'address': fields.Str(required=True, location='form'),
        'lng': fields.Float(required=True,location='form'),
        'lat': fields.Float(required=True,location='form'),
        'tags': fields.List(fields.String(),required=True,location='form'),
        'format': fields.Str(missing='json',location='query', validate=validate.Equal('json'))
    })
    def post(self, args):
        new_shop = Shop(name=args['name'],address=args['address'],lng=args['lng'],lat=args['lat'], withdrawn=False)
        new_shop.tags = [ShopTag(name=tag, shop=new_shop) for tag in args['tags'] if tag.strip()]
        db.session.add(new_shop)
        db.session.commit()
        return shop_schema.dump(new_shop).data

class ShopResource(Resource):
    @use_args({
	'format': fields.Str(location='query',validate=validate.Equal('json'))
    })
    def get(self, args, shop_id):
        shop = Shop.query.get_or_404(shop_id)
        return shop_schema.dump(shop).data
    
    @requires_auth
    @use_args({
        'name': fields.Str(required=True, location='form'),
        'address': fields.Str(required=True, location='form'),
        'lng': fields.Float(required=True,location='form'),
        'lat': fields.Float(required=True,location='form'),
        'tags': fields.List(fields.Str(),required=True,location='form'),
        'format': fields.Str(location='query', validate=validate.Equal('json'))
    })
    def put(self, args, shop_id):
        shop = Shop.query.get_or_404(shop_id)
        shop.name = args['name']
        shop.address = args['address']
        shop.lng = args['lng']
        shop.lat = args['lat']
        for tag in shop.tags:
            db.session.delete(tag)
        shop.tags = [ShopTag(name=tag, shop=shop) for tag in args['tags'] if tag.strip()]
        db.session.commit()
        return shop_schema.dump(shop).data
    
    @requires_auth
    @use_args({
        'name': fields.Str(location='form'),
        'address': fields.Str(location='form'),
        'lng': fields.Float(location='form'),
        'lat': fields.Float(location='form'),
        'tags': fields.List(fields.Str(),location='form'),
        'format': fields.Str(missing='json', location='query', validate=validate.Equal('json'))
    })
    def patch(self, args, shop_id):
        del args['format']
        if len(args) != 1:
            return 'Specify exactly one of: name, address, lng, lat, tags', 400
        shop = Shop.query.get_or_404(shop_id)
        changed = next(iter(args.keys()))
        if changed=='tags':
            for tag in shop.tags:
                db.session.delete(tag)
            shop.tags = [ShopTag(name=tag, shop=shop) for tag in args['tags'] if tag.strip()]
        else:
            setattr(shop, changed, args[changed])
        db.session.commit()
        return ShopSchema().dump(shop.data)
    
    @requires_auth
    @use_args({
        'format': fields.Str(missing='json', location='query', validate=validate.Equal('json'))
    })
    def delete(self, _args, shop_id,is_admin, **_kwargs):
        shop = Shop.query.get(shop_id)
        if not(shop):
            return {'message': "Shop not found on DB"},404 
        if is_admin:
            db.session.delete(shop)
        else:
            shop.withdrawn = True
        db.session.commit()
        return {'message': 'OK'}
