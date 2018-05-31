""" API Backend - Base Resource Models """

from flask_restful import Resource, abort
from api import api_rest
from api.security import multi_auth, restricted, restricted_or_current

class BaseResource(Resource):

    def options (self, *args, **kwargs):
        return None, 200, {
            'Allow': 'GET, POST, PUT, DELETE',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization,authorization,Token'
        }

    def get(self, *args, **kwargs):
        abort(405)

    def post(self, *args, **kwargs):
        abort(405)

    def put(self, *args, **kwargs):
        abort(405)

    def patch(self, *args, **kwargs):
        abort(405)

    def delete(self, *args, **kwargs):
        abort(405)

class SecureResource(BaseResource):
    method_decorators = [multi_auth.login_required]

def rest_resource(resource_cls):
    """ Decorator for adding resources to Api App """
    api_rest.add_resource(resource_cls, *resource_cls.endpoints)