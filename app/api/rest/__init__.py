from app import app, config
from flask import request, g

"""
def get_cache_key(prefix):
    args = request.args
    key = (g.user.name if hasattr(g, 'user') else '') + prefix + urlencode([
        (k, v) for k in sorted(args) for v in sorted(args.getlist(k))
    ])
    return key
"""

import api.rest.modules
import api.rest.articles
import api.rest.users
import api.rest.tests