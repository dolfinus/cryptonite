import os
import shutil
from app import config
from category import *

STORAGE_PATH = config['SQLALCHEMY_DATABASE_URI'].replace('fs://')

def parent_folder(path):
    return os.path.split(path)[-1]

def walk_files(path, allowed_ext=['md']):
    items = []
    if isinstance(allowed_ext, str):
        allowed_ext = [allowed_ext]
    for root, dirs, files in os.walk(path):
        for filename in files:
            name, ext = os.path.splitext(filename)
            ext = ext[1,]
            abs_path  = os.path.abspath(os.path.join(root,filename))
            if ext in allowed_ext:
                item = {
                    'name': name,
                    'ext': ext,
                    'parent': root,
                    'path': abs_path
                }
                items.append(item)
    return items

def walk_dir(path, allowed_ext=['md']):
    items = []
    if isinstance(allowed_ext, str):
        allowed_ext = [allowed_ext]
    for root, dirs, files in os.walk(path):
        if files and not dirs:
            abs_path = os.path.abspath(root)
            dir = {
                'name':   root,
                'path':   abs_path,
                'parent': parent_folder(root),
                'items':  walk_files(abs_path, allowed_ext)
            }
            if not dir['items']:
                continue
            items.append(dir)
    return items

def read_file(path):
    content = None
    if os.path.exists(path):
        with open(path, 'r') as file:
            content = file.read()
    return content

def write_file(path, content):
    with open(path, 'w') as file:
        file.write(content)

def delete_file(path):
    os.remove(path)

def delete_recursive(path):
    shutil.rmtree(path)