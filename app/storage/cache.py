
from app import app
import pylibmc
from functools import wraps
from inspect import getargspec
from flask import request, g

app.cache = pylibmc.Client(
    app.config['CACHE']['SERVERS'] or ['127.0.0.1:11211'],
    binary=app.config['CACHE']['BINARY'] or False,
    behaviors={k.lower():v for k,v in app.config['CACHE']['BEHAVIORS'].items()}
)

def cached(func, prefix='', arguments=[], force=False):
    @wraps(func)
    def f(*args, **kwargs):
        argspec = getargspec(func)

        http_args = request.args
        kw_args = {}
        kw_args.update(kwargs)
        func_args = {}
        for arg_name, arg in zip(argspec.args, args):
            if (len(arguments) > 0 and arg_name not in arguments):
                continue
            if arg_name == 'self':
                func_args[arg_name] = arg.__class__.__name__
            else:
                func_args[arg_name] = arg

        http_args = {k: v for k in sorted(http_args) for v in sorted(http_args.getlist(k))}
        http_headers = request.headers.__dict__
        func_args = {k: func_args[k] for k in sorted(func_args)}
        full_args = {
            'function_name' :func.__name__,
            'prefix': prefix,
            'current_user': (g.user.name if hasattr(g, 'user') and g.user is not None else 'anonymous')
        }
        full_args.update(func_args)
        full_args.update(http_args)
        full_args.update(http_headers)

        items = ['{}_{}'.format(str(k),str(v)) for k,v in full_args.items()]
        cache_key = str('_'.join(items).__hash__())

        if cache_key not in app.cache or force:
            app.cache[cache_key] = func(*args, **kwargs)
        return app.cache[cache_key]
    return f 

app.cached = cached