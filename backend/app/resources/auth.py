from functools import wraps
from flask import request
from app.models import User, db
from marshmallow import fields
from webargs.flaskparser import use_args
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from secrets import token_urlsafe

not_authorized = '', 403
bad_request = '', 400


def requires_auth(f):
    '''
    decorator to use for resources that need authorization
    adds 2 kwargs : is_admin, token
    '''
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-OBSERVATORY-AUTH')
        if not token:
            return {'errors': ['No authorization token provided']}, 403
        user = User.query.filter(User.token == token).first()
        if not user:
            return {'errors': ['Not authorized']}, 403
        kwargs['is_admin'] = user.is_admin
        kwargs['token'] = user.token
        return f(*args, **kwargs)
    return decorated


class LogoutResource(Resource):
    @requires_auth
    def post(self, token, **_kwargs):
        User.query.filter(User.token == token).update({'token': None})
        db.session.commit()
        return {'message': 'OK'}


class LoginResource(Resource):
    @use_args({
        'username': fields.Str(required=True, location='form'),
        'password': fields.Str(required=True, location='form')
    })
    def post(self, args):
        user = User.query.filter(User.username == args['username']).first()
        if not (user and user.verify_password(args['password'])):
            return not_authorized
        if user.token:
            return bad_request

        ready = False
        while not ready:
            ready = True
            token = token_urlsafe(20)
            user.token = token
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                ready = False
                # token collision

        return {'token': user.token}
