from functools import wraps
from secrets import token_urlsafe
from flask import request
from webargs import fields, validate
from webargs.flaskparser import use_args
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from app.models import User, db
from app.resources.utils import custom_error, ErrorCode


def requires_auth(f):
    '''
    decorator to use for resources that need authorization
    adds 2 kwargs : is_admin, token
    '''
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-OBSERVATORY-AUTH')
        if not token:
            return custom_error('token', ['No authorization token provided']), ErrorCode.FORBIDDEN
        user = User.query.filter(User.token == token).first()
        if not user:
            return custom_error('token', ['Invalid token']), ErrorCode.FORBIDDEN
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
        'password': fields.Str(required=True, location='form'),
        'format': fields.Str(missing='json', location='query', validate=validate.Equal('json'))
    })
    def post(self, args):
        user = User.query.filter(User.username == args['username']).first()
        if not user:
            return custom_error('username', ['Invalid username']), ErrorCode.BAD_REQUEST
        elif not user.verify_password(args['password']):
            return custom_error('password', ['Wrong password']), ErrorCode.BAD_REQUEST

        _login(user)

        return {'token': user.token}


class RegisterResource(Resource):
    @use_args({
        'username': fields.Str(required=True, location='form'),
        'password': fields.Str(required=True, location='form', validate=validate.Length(min=1)),
        'format': fields.Str(missing='json', location='query', validate=validate.Equal('json'))
    })
    def post(self, args):
        user = User(username=args['username'], password=args['password'])
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return custom_error('username', ['Username already in use']), ErrorCode.BAD_REQUEST

        return {'message': 'OK'}
