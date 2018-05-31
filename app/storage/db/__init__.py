import os
import re
from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from sqlalchemy.inspection import inspect
from sqlalchemy.ext.hybrid import hybrid_property
from flask_migrate import Migrate
from flask_sqlalchemy import BaseQuery
from storage.common.base import get_id, encode_datetime, divide_dict, Format
from storage.common.category import categorize

MIGRATIONS_DIR = '{}/migrations'.format(os.path.dirname(os.path.abspath(__file__)))

db = SQLAlchemy(app)
migrate = Migrate(app, db, directory=MIGRATIONS_DIR)

def generate_id(context):
    return get_id(context.get_current_parameters()['name'])

def call(object, callback, **kwargs):
  if not callback or not callable(callback):
    return
  for item in callback:
    function = item['func']
    pars     = item['params']
    params   = {}
    if pars:
        for name, value in kwargs.items():
            if name in pars:
                params[name] = value
    else:
      params = kwargs
    getattr(object, function)(**params)

class DbModel(object):
  def dict(self, filter=[], exclude=[]):
    result = {}
    mapper = inspect(self.__class__)
    for column in mapper.all_orm_descriptors.keys():
      value = getattr(self, column)
      if exclude and column in exclude:
        continue
      regex = re.compile('(\@?)('+column+')(\.?)(\w+)', flags=re.I+re.U)
      if isinstance(value, BaseQuery):
        children = value.all()
        for item in children:
          subfilter = []
          for field in filter:
            match = regex.match(field)
            if match:
              if match.group(1) == '@':
                if column not in result:
                  result[column] = []
                result[column].append(
                  item.dict(filter=match.group(4))[match.group(4)])
              else:
                subfilter.append(match.group(4))
          if subfilter:
            if column not in result:
              result[column] = []
            result[column].append(item.dict(filter=subfilter))
      elif isinstance(value, DbModel):
        subfilter = []
        for field in filter:
          match = regex.match(field)
          if match:
            if match.group(1) == '@':
              result[column] = value.dict(filter=match.group(4))[
                match.group(4)]
            else:
              subfilter.append(match.group(4))
        if subfilter:
          result[column] = value.dict(filter=subfilter)
      else:
        if column in filter:
          result[column] = getattr(self, column)
    return result

  def json(self, filter=[], exclude=[]):
      return encode_datetime(self.dict(filter=filter, exclude=exclude))

class Model:
  type     = None
  category = None
  items    = None
  hide     = None

  ids = ['id', 'name']
  filter = ['name', '@category.name', '@categories.name', 'category']

  save_callback   = None
  delete_callback = None

  def get_list(self, filter=[]):
      all_items = self.type.query.all()
      if not all_items:
          return {}
      if not filter:
        filter = ['name', '@category.name', 'category']
      items = {getattr(item, self.ids[0]): item.json(filter=filter) for item in all_items}
      return items

  def get_list_categorized(self, categories=[]):
      return categorize(self.get_list(), allowed_categories=categories)

  def get(self, format=Format.RAW, filter=[], **kwargs):
      item = self.type.query.filter_by(**kwargs).one_or_none()
      if not item:
          return None
      if not filter:
        filter = self.filter
      else:
        filter.extend(self.filter)
      if format == Format.RAW:
          return item
      if format == Format.DICT:
          return item.dict(filter=filter)
      if format == Format.JSON:
          return item.json(filter=filter)

  def is_exists(self, **kwargs):
      return self.get(**kwargs) is not None

  def read(self, **kwargs):
      item = self.get(format=Format.JSON, **kwargs)
      if not item:
          return {'error': '{0} {1} not found!'.format(self.type.__name__, kwargs)}, 404
      return item, 200

  def create(self, **kwargs):
      id, kwargs = divide_dict(kwargs, self.ids)
        
      if self.is_exists(**id):
          return {'error': '{0} with this {1!s} is already exists!'.format(self.type.__name__, id)}, 400
      session = db.session()
      if self.category:
          _category = None
          if 'category' in kwargs and kwargs['category']:
            _category = self.category.query.filter_by(name=kwargs['category']).one_or_none()
            if not _category:
                _category = self.category(name=kwargs['category'])
            del kwargs['category']
      if self.items and 'items' in kwargs and kwargs['items']:
        _items = kwargs['items']
        del kwargs['items']

      item = self.type(**id, **kwargs)
      call(item, self.save_callback, **kwargs)

      if self.category and _category:
          self.write(session, _category)
          item.category_id = _category.id
      if self.items and _items:
          for i, data in enumerate(_items):
            _item = self.items(item_no=i+1, **data)
            item.items.append(_item)
      self.write(session, item)
      return None, 201

  def update(self, **kwargs):
      id, kwargs = divide_dict(kwargs, self.ids)
  
      item = self.get(format=Format.RAW, **id)
      if not item:
          return {'error': '{} not found!'.format(self.type.__name__)}, 404
      session = db.session()
      if self.category:
          _category = None
          if 'category' in kwargs and kwargs['category']:
            _category = self.category.query.filter_by(name=kwargs['category']).one_or_none()
            if not _category:
                _category = self.category(name=kwargs['category'])
            del kwargs['category']
      if self.items and 'items' in kwargs and kwargs['items']:
        _items = kwargs['items']
        del kwargs['items']

      for param, value in kwargs.items():
        hide_default = ['category', 'categories', 'items']
        hide = self.hide or []
        hide.extend(hide_default)
        hide.extend(self.ids)
        if param not in hide:
          item.__setattr__(param, value)
      call(item, self.save_callback, **kwargs)

      
      if self.category:
          self.write(session, _category)
          item.category_id = _category.id
      if self.items and _items:
          item.items.delete()
          for i, data in enumerate(_items):
            _item = self.items(item_no=i+1, **data)
            item.items.append(_item)
      self.write(session, item)
      return None, 200

  def delete(self, **kwargs):
      id, kwargs = divide_dict(kwargs, self.ids)

      item = self.get(format=Format.RAW, **id)
      if not item:
          return {'error': '{} {} not found!'.format(self.type.__name__,name)}, 404
      session = db.session()
      call(item, self.delete_callback)
      self.remove(session, item)
      return None, 204

  def write(self, session, object):
    session.add(object)
    self.try_to_commit(session)

  def remove(self, session, object):
    session.delete(object)
    self.try_to_commit(session)

  @staticmethod
  def try_to_commit(session):
    try:
      session.commit()
    except exc.SQLAlchemyError as e:
      session.rollback()
      print(str(e))
