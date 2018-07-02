import os
import yaml
import shutil
from app import db, database
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from flask import request, g
from api.rest import config, cached
from api.rest.base import BaseResource, SecureResource, rest_resource
from urllib.parse import unquote
from transliterate import slugify

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
TESTS_DIR = CURR_DIR
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT='%y-%m-%dT%H:%M:%S'

#@cached
def get_tests(raw=False):
    categories = []
    empty_category = None
    for root, dirs, files in os.walk(TESTS_DIR):
        if os.path.abspath(os.path.join(root,'..')) == os.path.abspath(TESTS_DIR) and len(files) == 0 and len(dirs) > 0:
            dirname = os.path.split(root)[-1]
            category = {
                'id': slugify(dirname) or dirname.lower(),
                'title': dirname,
                'items': []
            }
            for subdirname in dirs:
                test = {}
                if raw:
                    config_path = os.path.abspath(os.path.join(root,subdirname,'config.yml'))
                    if os.path.exists(config_path):
                        with open(config_path,'r') as config_file:
                            test = yaml.load(config_file)
                test.update({
                    'id': slugify(subdirname) or subdirname.lower(),
                    'name': subdirname,
                    'items': []
                })
                for field, value in test.items():
                    if isinstance(value, datetime) or isinstance(value, date):
                        test[field] = test[field].isoformat()
                abs_subdir = os.path.abspath(os.path.join(root,subdirname))
                if raw:
                    test['path'] = abs_subdir
                for fullname in os.listdir(abs_subdir):
                    fullpath = os.path.abspath(os.path.join(abs_subdir,fullname))
                    if os.path.isfile(fullpath):
                        filename, ext = os.path.splitext(fullname)
                        if ext == '.md' and filename.isdigit:
                            item = {
                                'id': int(filename)
                            }
                            if raw:
                                item['path'] = fullpath
                            test['items'].append(item)
                category['items'].append(test)
            if raw:
                category['path'] = root
            if len(category['items']) > 0:
                categories.append(category)

    for root, dirs, files in os.walk(TESTS_DIR):
        if root == os.path.abspath(TESTS_DIR) and len(files) > 0 and len(dirs) == 0:
            empty_category = {
                'id': 'non-categorized',
                'title': 'Non-categorized',
                'items': []
            }
            for subdirname in dirs:
                test = {}
                if raw:
                    config_path = os.path.abspath(os.path.join(root,subdirname,'config.yml'))
                    if os.path.exists(config_path):
                        with open(config_path,'r') as config_file:
                            test = yaml.load(config_file)
                test.update({
                    'id': slugify(subdirname) or subdirname.lower(),
                    'name': subdirname,
                    'items': []
                })
                for field, value in test.items():
                    if isinstance(value, datetime) or isinstance(value, date):
                        test[field] = test[field].isoformat()
                abs_subdir = os.path.abspath(os.path.join(root,subdirname))
                if raw:
                    test['path'] = abs_subdir
                for fullname in os.listdir(abs_subdir):
                    fullpath = os.path.abspath(os.path.join(abs_subdir,fullname))
                    if os.path.isfile(fullpath):
                        filename, ext = os.path.splitext(fullname)
                        if ext == '.md' and filename.isdigit:
                            item = {
                                'id': int(filename)
                            }
                            if raw:
                                item['path'] = fullpath
                            test['items'].append(item)
                empty_category['items'].append(test)
            if raw:
                empty_category['path'] = root
            if len(empty_category['items']) > 0:
                categories.append(empty_category)
    return categories

def is_allowed(test):
    result = True
    if 'not_before' in test:
        if datetime.strptime(test['not_before'],DATE_FORMAT) > datetime.utcnow():
            result = False
    if 'not_after' in test:
        if datetime.strptime(test['not_after'],DATE_FORMAT) < datetime.utcnow():
            result = False
    return result

def is_over(test):
    if 'not_after' in test:
        if not isinstance(test['not_after'], datetime) or not isinstance(test['not_after'], date):
            test['not_after'] = datetime.strptime(test['not_after'], DATE_FORMAT)
        if test['not_after'] < datetime.utcnow():
            return True
        
    return False

def is_finished(test, test_result=None, user=None):
    if test_result is None:
        test_result = db.TestResult.query.filter_by(user_id = user.id, test_id = test['id']).first()
    if test_result is None:
        return False
    if 'max_duration' in test and datetime.utcnow() >= test_result.begin + relativedelta(minutes = int(test['max_duration'])):
        return True
    if test_result.is_finished:
        return True
    if test_result.last_item is not None:
        if 'items' in test and test_result.last_item > len(test['items']):
            return True
        if 'items_count' in test and test_result.last_item > test['items_count']:
            return True
    return False    

def get_allowed_tests(user):
    categories = get_tests()
    allowed_categories = []
    for category in categories:
        allowed_tests = []
        for test in category['items']:
            #is_finished = False
            #test_result = db.TestResult.query.filter_by(user_id = user.id, test_id = test['id']).first()
            #if test_result:
            #    is_finished = test_result.is_finished
            #if is_allowed(test) and not is_over(test) and not is_finished:
            if is_allowed(test) and not is_over(test) and not is_finished(test, user=g.user):
                allowed_tests.append(test)
        if len(allowed_tests) > 0:
            current_category = category
            current_category.update({'items': allowed_tests})
            allowed_categories.append(current_category)
    return allowed_categories


def get_test(id, raw=False):
    categories = get_tests(raw=True)
    for category in categories:
        for test in category['items']:
            if test['id'] == id:
                for i, item in enumerate(test['items']):
                    with open(item['path'],'r') as content:
                        test['items'][i]['content'] = content.read()
                        if not raw:
                            del test['items'][i]['path']
                if not raw:
                    del test['path']
                return test
    return None

@rest_resource
class TestsEdit(SecureResource):
    """ /api/tests/edit """
    endpoints = ['/tests/edit','/tests/edit/']

    #@cached
    def get(self):
        return get_tests()

    def post(self):
        if 'name' not in request.json:
            return {'error': 'Test name is empty!'}
        if 'items' not in request.json or len(request.json['items']) == 0:
            return {'error': 'Test items are empty!'}

        items    = request.json['items' ]
        name     = request.json['name'    ]
        category = request.json['category']

        id       = slugify(name) or name.lower()
        if get_test(id) is not None:
            return {'error': 'Test with this name is already exists!'}
        
        if 'category' in request.json:
            category_path = os.path.join(TESTS_DIR, category)
            if os.path.exists(category_path):
                if not os.path.isdir(category_path):
                    return {'error': 'Internal error!'}
            else:
                os.mkdir(category_path)
        else:
            category_path = TESTS_DIR
        test_path  = os.path.join(category_path, name)
        os.mkdir(test_path)

        for i, item in enumerate(items):
            item_path = '{}/{}.md'.format(test_path, str(i+1))
            with open(item_path,'w') as file:
                file.write(item['content'])

        config = {}
        for field in request.json:
            if field in ['max_duration', 'not_before', 'not_after']:
                config[field] = request.json[field]

        config_path = os.path.abspath(os.path.join(test_path,'config.yml'))
        with open(config_path,'w') as config_file:
            yaml.dump(config, config_file)

        return {}, 201

@rest_resource
class TestEdit(SecureResource):
    """ /api/tests/edit/name """
    endpoints = ['/tests/edit/<string:test>']

    #@cached
    def get(self, test):
        if g.user is None or not g.user.is_admin:
            return {'error': 'Access denied!'}, 401
        test_name = unquote(test)
        data = get_test(test_name)
        if data:
            return data
        else:
            return {'error': 'Test {} not found!'.format(test_name)}, 404

    def post(self, test):
        if g.user is None or not g.user.is_admin:
            return {'error': 'Access denied!'}, 401
        test_name = unquote(test)
        if 'items' not in request.json or len(request.json['items']) == 0:
            return {'error': 'Test items are empty!'}
        old_test = get_test(test_name, raw=True)
        if old_test is None:
            return {'error': 'Test {} not found!'.format(test_name)}, 404
        old_items = old_test['items']
        new_items = request.json['items']

        if old_items != new_items:
            for i, item in enumerate(new_items):
                item_path = os.path.join('{}/{}.md'.format(old_test['path'], item['id']))
                with open(item_path,'w') as file:
                    file.write(new_items[i]['content'])

        config = {}
        for field in old_test:
            if field in ['max_duration', 'not_before', 'not_after']:
                config[field] = old_test[field]
        for field in request.json:
            if field in ['max_duration', 'not_before', 'not_after']:
                config[field] = request.json[field]

        config_path = os.path.abspath(os.path.join(old_test['path'],'config.yml'))
        with open(config_path,'w') as config_file:
            yaml.dump(config, config_file)
        return {}, 200

    def delete(self, test):
        if not g.user.is_admin:
            return {'error': 'Access denied!'}, 401
        test_name = unquote(test)
        exist_test = get_test(test_name, raw=True)
        if exist_test is None:
            return {'error': 'Test {} not found!'.format(test_name)}, 404
        shutil.rmtree(exist_test['path'])

        return None, 204

@rest_resource
class TestsRun(SecureResource):
    """ /api/tests/run """
    endpoints = ['/tests/run','/tests/run/']

    #@cached
    def get(self):
        if g.user is None:
            return {'error': 'Access denied!'}, 401
        return get_allowed_tests(g.user)

@rest_resource
class TestRun(SecureResource):
    """ /api/tests/run/name """
    endpoints = ['/tests/run/<string:test>']

    #@cached
    def get(self, test):
        test_name = unquote(test)
        data = get_test(test_name)
        if g.user is None:
            return {'error': 'Access denied!'}, 401
        if data is None:
            return {'error': 'Test {} not found!'.format(test_name)}, 404
        data['items_count'] = len(data['items'])
        del data['items']
        test_result = db.TestResult.query.filter_by(user_id = g.user.id, test_id = data['id']).first()
        if test_result:
            data['is_finished'] = is_finished(data, test_result)
            data['last_item']   = test_result.last_item
            data['begin']       = test_result.begin.isoformat()
            data['end'  ]       = test_result.end.isoformat()
        return data

@rest_resource
class TestRunItem(SecureResource):
    """ /api/tests/run/name/id """
    endpoints = ['/tests/run/<string:test>/<int:id>']

    #@cached
    def get(self, test, id):
        if g.user is None:
            return {'error': 'Access denied!'}, 401

        test_name = unquote(test)
        data = get_test(test_name)
        if data is None:
            return {'error': 'Test {} not found!'.format(test_name)}, 404
        if id > len(data['items']):
            return {'error': 'Test {} item {} not found!'.format(test_name, str(id))}
        if not is_allowed(data):
            return {'error': 'Test {} cannot be run!'.format(test_name)}
        
        test_result = db.TestResult.query.filter_by(user_id = g.user.id, test_id = data['id']).first()
        if not test_result:
            test_result = db.TestResult(user_id = g.user.id, test_id = data['id'], score = 0, begin = datetime.utcnow(), end = datetime.utcnow())

        if is_finished(data, test_result):
            return {'error': 'Test {} is already finished!'.format(test_name)}
        
        if not test_result.last_item is None and test_result.last_item > id:
            return {'error': 'You cant read previous items!'}

        test_result.last_item = id
        session = database.session()
        try:
            session.add(test_result)
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
            return {'error': 'Internal error!'}, 500

        item = data['items'][id-1]
        item['content'] = item['content'].replace('[x]','[ ]').replace('[X]','[ ]').replace('[*]','[ ]').replace('(*)','( )')
        return item


    def post(self, test, id):
        test_name = unquote(test)
        data = get_test(test_name)
        session = database.session()
        if g.user is None:
            return {'error': 'Access denied!'}, 401
        if data is None:
            return {'error': 'Test {} not found!'.format(test_name)}
        if not is_allowed(data):
            return {'error': 'Test {} cannot is over!'.format(test_name)}
        if id > len(data['items']):
            return {'error': 'Test {} item {} not found!'.format(test_name, str(id))}

        test_result = db.TestResult.query.filter_by(user_id = g.user.id, test_id = data['id']).first()

        if test_result is None:
            return {'error': 'You should get test item before answer!'}
        
        if id < test_result.last_item:
            return {'error': 'Test {} item {} already saved!'.format(test_name, str(id))}
        test_result.is_finished = is_finished(data, test_result)
        if test_result.is_finished:
            try:
                session.add(test_result)
                session.commit()
            except Exception:
                session.rollback()
            return {'error': 'Test {} is over!'.format(test_name)}

        correct_answer = data['items'][id-1]['content']
        if 'answer' not in request.json or len(request.json['answer']) == 0:
            return {'error': 'Test {} item {} answer is empty!'.format(test_name, str(id))}
        answer = request.json['answer']

        if answer == correct_answer:
            test_result.score += 1

        if len(data['items']) <= id:
            test_result.is_finished = True
            test_result.last_item = id
        else:
            test_result.last_item = id + 1
        test_result.end = datetime.utcnow()

        item_result = db.TestAnswer(result_id = test_result.id, item_no = id-1, answer=answer, result = (answer == correct_answer), time = datetime.utcnow())

        try:
            session.add(item_result)
            session.add(test_result)
            session.commit()
            return {}, 200
        except Exception as e:
            session.rollback()
            print(e)
            return {'error': 'Internal error!'}

        return {}, 200


@rest_resource
class TestsRunResult(SecureResource):
    """ /api/tests/result or /api/tests/results """
    endpoints = ['/tests/results','/tests/results/','/tests/result','/tests/result/']

    #@cached
    def get(self):
        if g.user is None:
            return {'error': 'Access denied!'}, 401
        if g.user.is_admin:
            return get_tests()
        finished = {
            'id': 0,
            'title': 'Finished tests',
            'items': []
        }
        over = {
            'id': 0,
            'title': 'Time over tests',
            'items': []
        }
        tests = [test for category in get_tests() for test in category['items']]
        for test in tests:
            item = {}
            test_result = db.TestResult.query.filter_by(user_id = g.user.id, test_id = test['id']).first()
            if test_result is None:
                continue
            if not (is_finished(test, test_result) or is_over(test)):
                continue
            for field in test:
                if field in ['id', 'name']:
                    item[field] = test[field]

            if  is_finished(test, test_result):
                finished['items'].append(item)
            else:
                over['items'].append(item)

        result = []
        if len(finished['items']) > 0:
            result.append(finished)
        if len(over['items']) > 0:
            result.append(over)
        print(result)
        return result

@rest_resource
class TestRunResult(SecureResource):
    """ /api/tests/result/name """
    endpoints = ['/tests/result/<string:test>']

    #@cached
    def get(self, test):
        test_name = unquote(test)
        data = get_test(test_name)
        if g.user is None:
            return {'error': 'Access denied!'}, 401
        if data is None:
            return {'error': 'Test {} not found!'.format(test_name)}, 404
        test_result = db.TestResult.query.filter_by(user_id = g.user.id, test_id = data['id']).first()
        if test_result is None:
            return {'error': 'Test {} not fihisned!'.format(test_name)}
        if not (is_finished(data, test_result) or is_over(data)):
            return {'error': 'Test {} not fihisned!'.format(test_name)}

        item = {}
        for field in data:
            if field in ['id', 'name', 'max_duration', 'not_before', 'not_after']:
                if isinstance(data[field], datetime) or isinstance(data[field], date):
                    item[field] = data[field].isoformat()
                else:
                    item[field] = data[field]
        for field, value in test_result.__dict__.items():
            if field in ['begin', 'end', 'score', 'is_finished']:
                if isinstance(value, datetime) or isinstance(value, date):
                    item[field] = value.isoformat()
                else:
                    item[field] = value
        
        item['items_count'] = len(data['items'])
        item['answers'] = []
        if g.user.is_admin or is_over(data):
            for i in range(0, item['items_count']):
                ans = test_result.answers.filter_by(item_no = i).first()
                answer = {
                    'item_no': i+1,
                    'time':    None,
                    'answer':  '',
                    'result':  None
                }
                if ans:
                    answer['time']   = ans.time.isoformat()
                    answer['answer'] = ans.answer
                    answer['result'] = ans.result
                item['answers'].append(answer)

        return item

@rest_resource
class TestRunResults(SecureResource):
    """ /api/tests/results/name """
    endpoints = ['/tests/results/<string:test>']

    #@cached
    def get(self, test):
        test_name = unquote(test)
        data = get_test(test_name)
        if g.user is None or not g.user.is_admin:
            return {'error': 'Access denied!'}, 401
        if data is None:
            return {'error': 'Test {} not found!'.format(test_name)}, 404
        users = db.User.query.filter_by(is_admin=False)

        results = []
        for user in users:
            test_result = db.TestResult.query.filter_by(user_id = user.id, test_id = data['id']).first()
            result = {
                'user': {
                    'name':        user.name,
                    'first_name':  user.first_name,
                    'second_name': user.second_name,
                    'last_name':   user.last_name
                },
                'answers': [{'item_no': i+1, 'time': None, 'answer': '', 'result': None} for i in range(0, len(data['items']))],
                'begin': None,
                'end':   None,
                'score': 0,
                'is_finished': False
            }
            if test_result is None:
                results.append(result)
                continue
            for field, value in test_result.__dict__.items():
                if field in ['begin', 'end', 'score', 'is_finished']:
                    if isinstance(value, datetime) or isinstance(value, date):
                        result[field] = value.isoformat()
                    else:
                        result[field] = value
            for i in range(0, len(data['items'])):
                ans = test_result.answers.filter_by(item_no = i).first()
                if ans:
                    answer = {
                        'item_no': ans.item_no,
                        'time':    ans.time.isoformat(),
                        'answer':  ans.answer,
                        'result':  ans.result
                    }
                    result['answers'][i] = answer
            results.append(result)
        return {'id': data['id'], 'name': data['name'], 
                'items_count': len(data['items']), 'results': results}