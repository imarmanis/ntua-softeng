from flask_restful import Resource
from webargs import fields, validate
from webargs.flaskparser import use_args
from app.models import Price, db, ma
from sqlalchemy import func


class StatSchema(ma.ModelSchema):
    date = fields.Date()
    min = fields.Float()
    avg = fields.Float()
    max = fields.Float()


class Stat:
    def __init__(self, date_, min_, avg_, max_):
        self.date = date_
        self.min = min_
        self.avg = avg_
        self.max = max_


class StatsResource(Resource):

    @use_args({
        'dateFrom': fields.Date(required=True, location='query'),
        'dateTo': fields.Date(required=True, location='query'),
        'product': fields.Int(required=True, location='query'),
        'format': fields.Str(missing='json', location='query', validate=validate.Equal('json'))
    })
    def get(self, args):
        query = db.session.query(Price.date, func.min(Price.price), func.avg(Price.price), func.max(Price.price)).\
            filter(Price.product_id == args['product'], Price.date.between(args['dateFrom'], args['dateTo'])).\
            group_by(Price.date).order_by(Price.date.asc())
        stats = [Stat(*x) for x in query.all()]
        return StatSchema(many=True).dump(stats).data
