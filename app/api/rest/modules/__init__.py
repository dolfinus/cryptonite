import os
import inspect
import json
import pkgutil
from flask import request
import api
from api.rest import config
from api.rest.base import SecureResource, rest_resource
from storage.common.base import divide_dict

MODULES_PATH = 'api.rest.modules.'

__dict__ = {}
for importer, modname, ispkg in pkgutil.walk_packages(path=MODULES_PATH):
  if MODULES_PATH in modname and ispkg:
    module = __import__(modname)
    __dict__[modname.replace(MODULES_PATH,'')] = module
__all__ = [k for k in __dict__]

#@cached
def get_modules():
    return api.rest.modules.__all__

def get_module(name):
    return api.rest.modules.__dict__[name]

#@cached
def get_config(module_name, typenames=None):
    constructor = get_constructor(module_name)
    config = constructor.config()
    preserve_keys = ['id', 'init', 'categories']
    if type(typenames) == str:
        preserve_keys.append(typenames)
    elif type(typenames) == list:
        preserve_keys += typenames
    cfg = {k: config[k] for k in preserve_keys if k in config}
    return cfg

def get_constructor(module_name):
    for name, obj in inspect.getmembers(get_module(module_name)):
        if name in ['Alphabet']:
            continue
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

def first(dict_):
  return dict_[list(dict_.keys())[0]]

#@cached
def check_module(module_name, allowed_types):
    return module_name in get_allowed_modules(allowed_types)

class Modules_(SecureResource):
    """ /api/modules """
    endpoints = ['/modules/']
    allowed_types = ['cipher', 'eds']

    #@cached
    def get(self):
        modules = [module for module in get_allowed_modules(self.allowed_types)]
        configs = [get_config(module, self.allowed_types) for module in modules]
        if (request.args.get('categorized', False, bool)):
            allowed_categories = request.args['categories[]'] or request.args['categories'] or ['stream', 'block', 'transition']
            categories = {}
            for config in configs:
                for category in config['categories']:
                    if category in allowed_categories:
                        if category not in categories:
                            categories[category] = []
                        categories[category].append({'id': config['id'], 'name': config['id']})
            return [{'id': name, 'title': name, 'items': items} for name, items in categories.items()]
        else:
            return modules

class Module_(SecureResource):
    """ /api/modules/module """
    endpoints = ['/modules/<string:module>']
    allowed_types = ['cipher', 'eds']

    #@cached
    def get(self, module):
        if check_module(module, self.allowed_types):
            return get_config(module, self.allowed_types)
        else:
            return {'error': 'Module {} not found!'.format(module)}, 404

    def post(self, module):
        if check_module(module, self.allowed_types):
            config = get_config(module, self.allowed_types)
            data   = request.json.copy()

            action, data = divide_dict(data, 'action')
            if not action:
                return {'error': 'Action not set!'}
            
            actions, _ = divide_dict(config, self.allowed_types)
            if not action in first(actions):
                return {'error': 'Wrong action {}!'.format(action)}
            init   = {}
            if 'init' in config:
              for item in config['init']:
                param = item['name']
                if param in data:
                  init[param] = data[param]
                else:
                  return {'error': 'Missing init param {}!'.format(param)}

            _, data = divide_dict(data, list(init.keys()))

            opentext, params = divide_dict(data, 'content')
            """
            if not opentext:
                file = request.files['file']
                file_bytes = file.read(config['MAX_FILE_SIZE'])
                if bool(file.filename):
                    opentext = json.loads(file_bytes.decode('utf-8'))
            """
            if not opentext:
                return {'error': 'You should set input text or upload file!'}
            print(action)
            print(init)
            print(params)
            print(opentext)
            constructor = get_constructor(module)
            singletone  = constructor(**init)
            return getattr(singletone, action, None)(opentext, **dict(params))
        return {'error': 'Module {} not found!'.format(module)}, 404

@rest_resource
class Modules(Modules_):
    """ /api/modules """
    endpoints = ['/modules','/modules/']
    allowed_types = ['cipher', 'eds']

@rest_resource
class Module(Module_):
    """ /api/modules/module """
    endpoints = ['/modules/<string:module>']
    allowed_types = ['cipher', 'eds']

@rest_resource
class Ciphers(Modules_):
    """ /api/ciphers """
    endpoints = ['/ciphers','/ciphers/']
    allowed_types = ['cipher']

@rest_resource
class Cipher(Module_):
    """ /api/ciphers/name """
    endpoints = ['/ciphers/<string:module>']
    allowed_types = ['cipher']

@rest_resource
class EDS(Modules_):
    """ /api/eds """
    endpoints = ['/eds','/eds/']
    allowed_types = ['eds']

@rest_resource
class DS(Module_):
    """ /api/eds/name """
    endpoints = ['/eds/<string:module>']
    allowed_types = ['eds']