from flask import request, g
from api.rest.base import  SecureResource, rest_resource, restricted, restricted_or_current
from storage import UserSingletone as _Users
from storage.common.category import categorize

@rest_resource
class Users(SecureResource):
    """ /api/users """
    endpoints = ['/users','/users/']

    #@cached
    @restricted
    def get(self):
        if ('categorized' in request.args):
            allowed_categories = request.args.get('categories[]', [], dict) or request.args.get('categories', [], dict) or []
            return _Users.get_list_categorized(allowed_categories)
        return [k for k in _Users.get_list()]

    @restricted
    def post(self):
        if 'name' not in request.json:
            return {'error': 'User name is empty!'}
        if 'password' not in request.json:
            return {'error': 'User password is empty!'}

        name     = request.json['name'    ].strip()
        params = {
            'is_admin': False,
            'password': ''
        }
        for field, value in request.json.items():
            if field != 'name':
                params[field] = value

        return _Users.create(name=name, **params)

@rest_resource
class User(SecureResource):
    """ /api/modules/users """
    endpoints = ['/users/<string:name>']

    #@cached
    @restricted_or_current
    def get(self, name):
        return _Users.read(name=name)

    @restricted_or_current
    def put(self, name):
        params = {}
        for field, value in request.json.items():
            if field != 'name' and not (field == 'is_admin' and not g.user.is_admin):
                params[field] = value
        return _Users.update(name=name, **params)

    @restricted
    def delete(self, name):
        return _Users.delete(name=name)
