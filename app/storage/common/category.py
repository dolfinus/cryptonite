from .base import get_id

def categorize(items, field='category', allowed_categories=None):
    categories = {}
    for id, item in items.items():
        if (not field in item) or (not item[field]):
            item[field] = ['Non-categorized']
        if isinstance(item[field], str):
            item[field] = [item[field]]
        for category in item[field]:
            if (isinstance(allowed_categories, list) and category.lower() in allowed_categories) or (not allowed_categories):
                if category not in categories:
                    categories[category] = []
                categories[category].append({'id': id, 'name': item['name']})
    return [{'id': get_id(k), 'title': k, 'items': v} for k, v in categories.items()]
