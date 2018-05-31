from storage import TestSingletone as _Tests, TestItemSingletone as _TestItems, TestResultSingletone as _TestResults, TestAnswerSingletone as _TestAnswers, UserSingletone as _Users
from storage.common.category import categorize
from storage.common.base import strip_spaces
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from flask import request, g
from api.rest.base import SecureResource, rest_resource, restricted, restricted_or_current

DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT='%Y-%m-%dT%H:%M:%S'

def items_empty(json):
    return 'items' not in json or len(json['items']) == 0

@rest_resource
class TestsEdit(SecureResource):
    """ /api/tests/edit """
    endpoints = ['/tests/results','/tests/results/','/tests/edit','/tests/edit/']

    #@cached
    def get(self):
        if ('categorized' in request.args):
            allowed_categories = request.args.get('categories[]', [], dict) or request.args.get('categories', [], dict) or []
            return _Tests.get_list_categorized(allowed_categories)
        return list(_Tests.get_list())

    def post(self):
        if 'name' not in request.json:
            return {'error': 'Test name is empty!'}
        if items_empty(request.json):
            return {'error': 'Test items are empty!'}

        items        = request.json['items'       ]
        name         = request.json['name'        ].strip()
        max_duration = request.json['max_duration'].strip() or None
        not_before   = request.json['not_before'  ].strip() or None
        not_after    = request.json['not_after'   ].strip() or None
        category     = request.json['category'    ].strip() or None
        params       = {}

        if max_duration:
            params['max_duration'] = int(max_duration)
        if not_before:
            params['not_before']   = datetime.strptime(not_before, DATE_FORMAT)
        if not_after:
            params['not_after']    = datetime.strptime(not_after,  DATE_FORMAT)

        return _Tests.create(name=name, category=category, items=items, **params)

@rest_resource
class TestEdit(SecureResource):
    """ /api/tests/edit/name """
    endpoints = ['/tests/edit/<string:id>']

    #@cached
    @restricted
    def get(self, id):
        return _Tests.read(id=id, filter=['items.item_no', 'items.content'])

    @restricted
    def put(self, id):
        if items_empty(request.json):
            return {'error': 'Test items are empty!'}

        items        = request.json['items'       ]
        max_duration = request.json['max_duration'].strip() or None
        not_before   = request.json['not_before'  ].strip() or None
        not_after    = request.json['not_after'   ].strip() or None
        category     = request.json['category'    ].strip() or None
        params       = {}

        if max_duration:
            params['max_duration'] = int(max_duration)
        if not_before:
            params['not_before']   = datetime.strptime(not_before, DATE_FORMAT)
        if not_after:
            params['not_after']    = datetime.strptime(not_after,  DATE_FORMAT)

        return _Tests.update(id=id, category=category, items=items, **params)

    @restricted
    def delete(self, id):
        return _Tests.delete(id=id)

@rest_resource
class TestsRun(SecureResource):
    """ /api/tests/run """
    endpoints = ['/tests/run','/tests/run/']

    #@cached
    def get(self):
        if ('categorized' in request.args):
            allowed_categories = request.args.get('categories[]', [], dict) or request.args.get('categories', [], dict) or []
            return _Tests.get_allowed_categorized(user_id=g.user.id, categories=allowed_categories)
        return list(_Tests.get_allowed_list(user_id=g.user.id))

@rest_resource
class TestRun(SecureResource):
    """ /api/tests/run/name """
    endpoints = ['/tests/run/<string:id>']

    #@cached
    def get(self, id):
        return _Tests.get_allowed(id=id, user_id=g.user.id)

@rest_resource
class TestRunItem(SecureResource):
    """ /api/tests/run/name/no """
    endpoints = ['/tests/run/<string:id>/<int:no>']

    #@cached
    def get(self, id, no):
        no = int(no)
        test, return_code = _Tests.get_allowed(id=id, user_id=g.user.id)
        if return_code != 200:
            return test, return_code

        test_item, return_code = _TestItems.read(test_id=id, item_no=no)
        if return_code != 200:
            return test, return_code

        test_result, return_code = _TestResults.read(test_id=id, user_id=g.user.id)
        if return_code == 404:
            test_result, return_code = _TestResults.create(test_id=id, user_id=g.user.id, begin = datetime.utcnow().replace(microsecond=0), end = datetime.utcnow().replace(microsecond=0))
            if return_code != 201:
                return test_result, return_code
            test_result, return_code = _TestResults.read(test_id=id, user_id=g.user.id)

        if _TestResults.is_finished(result=test_result):
            return {'error': 'Test {} is already finished!'.format(id)}, 400

        if test_result['last_item'] > no:
            return {'error': 'You cant read previous items!'}, 400

        update_result, result_code = _TestResults.update(test_id=id, user_id=g.user.id, last_item = no)
        if result_code != 200:
            return update_result, result_code

        return _TestItems.get_unmasked(test_id=id, item_no=no)

    def post(self, id, no):
        no = int(no)
        test, return_code = _Tests.get_allowed(id=id, user_id=g.user.id)
        if return_code != 200:
            return test, return_code

        if no > test['items_count']:
            return {'error': 'Test {} item {} not found!'.format(id, str(no))}, 400

        #if 'answer' not in request.json or len(request.json['answer']) == 0:
        #    return {'error': 'Test {} item {} answer is empty!'.format(id, str(no))}
        if not 'answer' in request.json:
            request.json['answer'] = ''

        test_item, return_code = _TestItems.read(test_id=id, item_no=no)
        if return_code != 200:
            return test_item, return_code

        test_result, return_code = _TestResults.read(test_id=id, user_id=g.user.id)
        if return_code == 404:
            return {'error': 'You should get test item before answer!'}, 400
        
        is_finished = test_result['is_finished']
        if is_finished:
            return {'error': 'Test {} is over!'.format(id)}, 200

        _TestResults.set_finished(test_id=id, user_id=g.user.id)

        answer  = request.json['answer']
        correct_answer = test_item['content']
        score     = test_result['score']
        last_item = no + 1
        result = strip_spaces(answer) == strip_spaces(correct_answer)

        test_answer, return_code = _TestAnswers.create(item_id = test_item['id'], result_id = test_result['id'], answer=answer, result = result)
        if return_code != 201:
            return test_item, return_code

        test_result, return_code = _TestResults.update(test_id=id, user_id=g.user.id, last_item=last_item)
        if return_code != 200:
            return test_result, 400
        return _TestResults.set_finished(test_id=id, user_id=g.user.id)


@rest_resource
class TestsRunResult(SecureResource):
    """ /api/tests/result or /api/tests/results """
    endpoints = ['/tests/result','/tests/result/']

    #@cached
    def get(self):
        if ('categorized' in request.args):
            allowed_categories = request.args.get('categories[]', [], dict) or request.args.get('categories', [], dict) or []
            return _TestResults.get_results_categorized(user_id=g.user.id, categories=allowed_categories)
        return list(_TestResults.get_results_list(user_id=g.user.id))

@rest_resource
class TestRunResult(SecureResource):
    """ /api/tests/result/name """
    endpoints = ['/tests/result/<string:id>']

    #@cached
    def get(self, id):
        return _TestResults.get_result(test_id=id, user_id=g.user.id)

@rest_resource
class TestRunResults(SecureResource):
    """ /api/tests/results/name """
    endpoints = ['/tests/results/<string:id>']

    #@cached
    @restricted
    def get(self, id):
        results = []
        users = _Users.get_list()
        test, return_code = _Tests.read(id=id)
        if return_code != 200:
            return test, return_code
        for user_id in users:
            user, return_code = _Users.read(id=user_id)
            user_result, return_code = _TestResults.read(test_id=id, user_id=user_id, filter=['name', 'first_name', 'second_name', 'last_name'])
            result = {
                'user': user,
                'answers': [],
                'begin': None,
                'end':   None,
                'score': 0,
                'is_finished': False
            }
            if return_code == 200:
                result.update(user_result)
                for i in range(0, test['items_count']):
                    item, return_code = _TestItems.read(test_id=id, item_no=i+1)
                    if return_code == 200:
                        answer = {
                            'item_no': i+1,
                            'time': None,
                            'answer': '',
                            'result': None
                        }
                        user_answer, return_code = _TestAnswers.read(item_id=item['id'], result_id=user_result['id'])
                        if return_code == 200:
                            answer.update(user_answer)
                        result['answers'].append(answer)
            results.append(result)
        
        results_formatted = {
            'id':   id,
            'name': test['name'],
            'items_count': test['items_count'],
            'results': results
        }
        return results_formatted
        