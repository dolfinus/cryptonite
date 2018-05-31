import os
from config import config
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from storage.common.base import unmask
from storage.db.test import Tests, TestResults, TestAnswers, TestItems

from .base import Format
from .category import categorize

DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT="%Y-%m-%dT%H:%M:%S"

TestAnswerSingletone = TestAnswers()

class _TestSingletone(Tests):
    def is_planned(self, id):
      test = self.get(id=id, format=Format.RAW)
      if not test:
        return False
      if test.not_before is not None and test.not_before > datetime.utcnow().date():
        return True
      return False

    def is_over(self, id):
      test = self.get(id=id, format=Format.RAW)
      if not test:
        return False
      if test.not_after is not None and test.not_after < datetime.utcnow().date():
        return True
      return False
    
    def is_allowed(self, id):
      return not(self.is_planned(id) or self.is_over(id))
    
    def get_allowed(self, id, user_id):
      test, return_code = self.read(id=id)
      if return_code != 200:
        return test, return_code

      if 'items' in test:
        del test['items']

      if self.is_allowed(id=id):
        result, return_code = TestResultSingletone.read(test_id=id, user_id=user_id)
        if return_code != 200:
          return test, 200
        test['last_item'] = result['last_item']
        test['begin'    ] = result['begin'    ]
        test['end'      ] = result['end'      ]
      return test, return_code

    def get_allowed_list(self, user_id):
      result = {}
      tests = self.get_list()
      for id, test in tests.items():
        is_allowed =self.is_allowed(id=id)
        is_finished = TestResultSingletone.is_finished(test_id=id, user_id=user_id)
        if is_allowed and not is_finished:
            result[id] = test
      return result
    
    def get_allowed_categorized(self, user_id, categories=None):
        return categorize(self.get_allowed_list(user_id=user_id), allowed_categories=categories)

class _TestResultSingletone(TestResults):
    save_callback = [{
      'func': 'set_finished',
      'params': []
    }]

    def is_finished(self, result=None, test_id=None, user_id=None):
      if result is None:
        test = TestSingletone.get(id=test_id, format=Format.DICT)
        result = self.get(test_id=test_id, user_id=user_id, format=Format.DICT)
      else:
        test = TestSingletone.get(id=result['test_id'], format=Format.DICT)
      if not test:
        return False
      if result is None:
        return False
      begin = result['begin']
      if isinstance(begin, str):
        begin = datetime.strptime(begin, DATETIME_FORMAT)
      if test['max_duration'] is not None and datetime.utcnow() >= begin + relativedelta(minutes = int(test['max_duration'])):
        return True
      if result['is_finished']:
        return True
      if result['last_item'] is not None:
        if result['last_item'] > test['items_count']:
          return True
      return False

    def set_finished(self, test_id=None, user_id=None, result=None):
      if result is None:
        result, code = self.read(test_id=test_id, user_id=user_id)
        if code != 200:
          return result, code
      else:
        test_id = result['test_id']
        user_id = result['user_id']
      is_finished = self.is_finished(result = result)
      self.update(test_id=test_id, user_id=user_id, is_finished=is_finished)
      return None, 200

    def get_result(self, test_id=None, user_id=None, result=None):
      if result is None:
        test, return_code = TestSingletone.read(id=test_id)
        if return_code != 200:
          return test, return_code
        result, return_code = self.read(test_id=test_id, user_id=user_id)
        if return_code != 200:
          return test, return_code
      else:
        test, return_code = TestSingletone.read(id=result['test_id'])
        if return_code != 200:
          return test, return_code
        

      is_finished = self.is_finished(result=result)
      is_over = TestSingletone.is_over(id=test_id)
      if not (is_finished or is_over):
          return {'error': 'Test {} not fihisned!'.format(test_id)}, 400

      test.update(result)
      return test, 200

    def get_results_list(self, user_id):
      result = {}
      tests = TestSingletone.get_list()
      for id, test in tests.items():
        is_finished = self.is_finished(test_id=id, user_id=user_id)
        is_over = TestSingletone.is_over(id=id)
        if is_finished or is_over:
          user_result, code = self.read(test_id=id, user_id=user_id)
          if code == 200:
            test['category'] = user_result['category']
          result[id] = test
      return result
    
    def get_results_categorized(self, user_id, categories=None):
        return categorize(self.get_results_list(user_id=user_id), allowed_categories=categories)

class _TestItemSingletone(TestItems):
    def get_unmasked(self, test_id, item_no):
      item, result_code = self.read(test_id=test_id, item_no=item_no)
      if result_code != 200:
        return item, result_code
      item['content'] = unmask(item['content'])
      return item, result_code

TestSingletone = _TestSingletone()
TestResultSingletone = _TestResultSingletone()
TestItemSingletone = _TestItemSingletone()