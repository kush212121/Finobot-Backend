import json


def type_error():
    error_res = {'reply': 'Please Re-Enter The Text Again',
                 'tag': 'false', 'is_multi': 'false'}
    error_res = json.dumps(error_res)
    return error_res


def index_error():
    error_res = {'reply': ' Intent For This Field Is Not Added To Database. With Time We Will Get Smarter 😎',
                 'tag': 'flase', 'is_multi': 'false'}
    error_res = json.dumps(error_res)
    return error_res


def index_error_multi():
    error_res = 'Intent For This Field Is Not Added To Database. With Time We Will Get Smarter 😎'
    return error_res
