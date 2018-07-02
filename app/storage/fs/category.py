import os

def create_category(path, name):
    category_path = os.path.join(path, '/', name)
    if os.path.exists(category_path):
        if not os.path.isdir(category_path):
            return Exception('Wrong category name')
    else:
        os.mkdir(category_path)
    return category_path