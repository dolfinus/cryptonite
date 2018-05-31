from functools import wraps
from flask_restful import abort
from flask import request, g
from app import config
from storage import UserSingletone as _Users
from storage.common.base import Format
#from storage.cache import cached
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from itsdangerous import TimedJSONWebSignatureSerializer as JWT

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)

jwt = JWT(config['SECRET_KEY'], expires_in=config['SECRET_EXPIRES'])

@basic_auth.verify_password
def verify_password(username, password):
    g.user = None
    result = _Users.verify_password(id=username, password=password)
    if result:
        g.user = _Users.get(id=username)
    return result

@token_auth.verify_token
#@cached
def verify_token(token):
    g.user = None
    try:
        data = jwt.loads(token)
    except:
        return False
    if 'username' in data:
        user = _Users.get(id=data['username'])
        if user is not None:
            g.user = user
        return True
    return False

def restricted(func):
    @wraps(func)
    def f(*args, **kwargs):
        if not g.user.is_admin:
            return {'error': 'Access denied!'}, 401
        return func(*args, **kwargs)
    return f

def restricted_or_current(func):
    @wraps(func)
    def f(*args, **kwargs):
        if not g.user.is_admin and not g.user.name == kwargs['name']:
            return {'error': 'Access denied!'}, 401
        return func(*args, **kwargs)
    return f 
"""
@token_auth.verify_token
def token_error(code):
    return {'error': 'User not found!'}, 401

@basic_auth.error_handler
def auth_error():
    return {'error': 'User not found!'}, 401
"""