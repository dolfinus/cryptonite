import os
from flask import Blueprint, session, current_app, g
from flask_restful import Api
from itsdangerous import TimedJSONWebSignatureSerializer as JWT

api_bp = Blueprint('api_bp', __name__,
    template_folder='templates',
    url_prefix='/api'
)
api_rest = Api(api_bp)

# OPTIONAL
@api_bp.before_request
def set_user():
    if not hasattr(g, 'user'):
        g.user = None
    return

@api_bp.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = True
    response.headers['Access-Control-Expose-Headers'] = 'Content-Type,Token'
    if response.status_code < 400 and hasattr(g, 'user') and g.user is not None:
        jwt = JWT(current_app.config['SECRET_KEY'], expires_in=86400)
        response.headers['Token'] = jwt.dumps({'username': g.user.name})
    return response

from api import views, rest