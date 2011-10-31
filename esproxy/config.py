import re

allowed_paths = {
    'GET': [
        re.compile(r'^/(.*?)/(.*?)/(_count|_search)'),
    ],
}