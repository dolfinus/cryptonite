import os
import yaml
from base import *

TESTS_DIR = os.path.join(STORAGE_PATH, 'tests')
TEST_EXT  = 'md'
CONFIG_NAME = 'config.yml'
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT='%y-%m-%dT%H:%M:%S'

def get_tests(raw=False):
    tests = {}
    dirs = walk_dir(TESTS_DIR)
    for dir in dirs:
        id = get_id(dir.name)
        test = {
            'name': dir.name
        }
        config_path = get_config_path(parent_folder(dir.path))
        config = read_file(config_path)
        if config:
            test.update(yaml.load(config))
        if raw:
            test['path'] = dir.path
        root = parent_folder(parent_folder(dir.path))
        if root == TESTS_DIR:
            test['categories'] = []
        else:
            test['categories'] = [dir.parent]
        if id in tests:
            test['items_count'] = len(dir.items)
        
        tests[id] = test
    return tests

def get_test(id, raw=False):
    tests = get_tests(raw=True)
    if id in tests:
        test = tests[id]
        test['items'] = []
        for i in range(test['items_count']):
            item_path = get_item_path(test['path'], i)
            item = {
                'id': id,
                'content': read_file(item_path)
            }
            if raw:
                item['path'] = item_path
            test['items'].append(item)
        if not raw:
            del test['path']
        return test
    return None

def read_test(name):
    id   = get_id(name)
    test = get_test(id)
    if not test:
        return {'error': 'Test {} not found!'.format(id)}, 404
    return encode_datetime(article), 200

def create_test(name, items, category='', max_duration=None, not_before=None, not_after=None):
    id = get_id(name)
    category_path = TESTS_DIR
    if category:
        category_path = create_category(category_path, category)
    path = os.path.join(category_path, '/', id)
    save_test(path, items, max_duration, not_before, not_after)
    return {}, 201

def update_test(id, items, max_duration=None, not_before=None, not_after=None):
    test = get_tests(id)
    if not test:
        return {'error': 'Article {} not found!'.format(id)}, 404
    save_test(test['path'], items, max_duration, not_before, not_after)
    return {}, 200

def save_test(path, items, max_duration, not_before, not_after):
    for i, item in enumerate(items):
        item_path = get_item_path(path, i)
        write_file(item_path, item['content'])
    test = {}
    if max_duration:
        test['max_duration'] = max_duration
    if not_before:
        test['not_before']   = not_before
    if not_after:
        test['not_after']    = not_after
    if test:
        config_path = get_config_path(path)
        write_file(config_path, test)

def get_item_path(path, i):
    return os.path.join(path, '{}.{}'.format(i, TEST_EXT))

def get_config_path(path):
    return os.path.join(path, CONFIG_NAME)