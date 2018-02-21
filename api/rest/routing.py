"""
REST API Resource Routing

http://flask-restful.readthedocs.io/en/latest/
"""
import app
from flask import request
from api.rest.base import BaseResource, SecureResource, rest_resource
import inspect
import json
import api.rest.modules
from api.rest.modules import *

MAX_FILE_SIZE = 1 * 1026 * 1024 * 1024

def get_modules():
    return api.rest.modules.__all__

def get_module(name):
    return api.rest.modules.__dict__[name]

def get_config(module_name, typenames=None):
    constructor = get_constructor(module_name)
    config = constructor.config()
    preserve_keys = ['name', 'init']
    if type(typenames) == str:
        preserve_keys.append(typenames)
    elif type(typenames) == list:
        preserve_keys += typenames
    cfg = {k: config[k] for k in preserve_keys if k in config}
    return cfg

def get_constructor(module_name):
    for name, obj in inspect.getmembers(get_module(module_name)):
        if inspect.isclass(obj) and 'config' in obj.__dict__:
            return obj

def get_type_modules(type_name):
    for module in get_modules():
        config = get_config(module, type_name)
        if type_name in config:
            yield module

def get_allowed_modules(allowed_types):
    for allowed in allowed_types:
        for module in get_type_modules(allowed):
            yield module

def check_module(module, allowed_types):
    return module in get_allowed_modules(allowed_types)

def divide_dict(dict, names):
    if type(names) == str:
        names = [names]
    for name in names:
        if name in dict:
            eq     = dict[name]
            non_eq = dict.copy(); del dict[name]
        else:
            eq     = None
            non_eq = dict
    return eq, non_eq

class Modules_(BaseResource):
    """ /api/modules """
    endpoints = ['/module/']
    allowed_types = ['cipher', 'eds']

    def get(self, *args, **kwargs):
        return [module for module in get_allowed_modules(self.allowed_types)]

class Module_(BaseResource):
    """ /api/modules/module """
    endpoints = ['/modules/<string:module>']
    allowed_types = ['cipher', 'eds']  

    def get(self, module, *args, **kwargs):
        if check_module(module, self.allowed_types):
            return [get_config(module, self.allowed_types)]
        return {'error': 'Module {} not found!'.format(module)}

    def post(self, module, *args, **kwargs):
        if check_module(module, self.allowed_types):
            config = get_config(module, self.allowed_types)

            action = request.args['action']
            init   = request.args.copy(); del init['action']; init = {k:v for k,v in init.items()}
            print(request.data)
            print(request.args)
            print(request.files)
            print(request.form)
            opentext, params = divide_dict((request.json or request.form), 'input')
            if not opentext:
                file = request.files['file']
                file_bytes = file.read(MAX_FILE_SIZE)
                if bool(file.filename):
                    opentext = json.loads(file_bytes.decode('utf-8'))
            if not opentext:
                return {'error': 'You should set input text or upload file!'}

            params = {k:v for k,v in params.items()}
            print(params)
            actions, _ = divide_dict(config, self.allowed_types)
            if action in actions:
                constructor = get_constructor(module)
                singletone  = constructor(**init)
                return getattr(singletone, action, None)(opentext, **dict(params))
            else:
                return {'error': 'Wrong action {}!'.format(action)}
        return {'error': 'Module {} not found!'.format(module)}

@rest_resource
class Modules(Modules_):
    """ /api/modules """
    endpoints = ['/modules']
    allowed_types = ['cipher', 'eds']

@rest_resource
class Module(Module_):
    """ /api/modules/module """
    endpoints = ['/modules/<string:module>']
    allowed_types = ['cipher', 'eds']

@rest_resource
class Ciphers(Modules_):
    """ /api/ciphers """
    endpoints = ['/ciphers/']
    allowed_types = ['cipher']

@rest_resource
class Cipher(Module_):
    """ /api/ciphers/name """
    endpoints = ['/ciphers/<string:module>']
    allowed_types = ['cipher']

@rest_resource
class EDSs(Modules_):
    """ /api/eds """
    endpoints = ['/eds/']
    allowed_types = ['eds']

@rest_resource
class EDS(Module_):
    """ /api/eds/name """
    endpoints = ['/eds/<string:module>']
    allowed_types = ['eds']