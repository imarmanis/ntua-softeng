from functools import wraps
from secrets import token_urlsafe
from flask import request
from marshmallow import fields
from webargs.flaskparser import use_args
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from app.models import User, db

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


def _login(user):
    '''
    Actually log the user in.
    :param user: an User instance already in the db, but not already logged in
        (user.token should be None).
    '''
    while True:
        user.token = token_urlsafe(20)
        try:
            db.session.commit()
            break
        except IntegrityError:
            db.session.rollback()
            # token collision


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
        # Add format, like in the other resources, just to return bad request if it is XML?
    })
    def post(self, args):
        user = User.query.filter(User.username == args['username']).first()
        if not (user and user.verify_password(args['password'])):
            return not_authorized

        _login(user)

        return {'token': user.token}


class RegisterResource(Resource):
    @use_args({
        'username': fields.Str(required=True, location='form'),
        'password': fields.Str(required=True, location='form')
        # Add format, like in the other resources, just to return bad request if it is XML?
    })
    def post(self, args):
        user = User(username=args['username'], password=args['password'])
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            # username is in use
            db.session.rollback()
            return bad_request

        return {'token': user.token}
