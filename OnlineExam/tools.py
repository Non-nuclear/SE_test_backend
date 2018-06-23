from django.http import JsonResponse
from django.core.paginator import Paginator
from itertools import chain
import json
import datetime


def json_request(viewFunction):
    def _wrapped(request, *args, **kwargs):
        if request.method=='POST':
            request.json = json.loads(request.body.decode())
        return viewFunction(request, *args, **kwargs)
    return _wrapped


class GeneralResponse(JsonResponse):
    def __init__(self, status=True, payload=None):
        ret = {}
        if status is False:
            ret['status'] = 'error'
        else:
            ret['status'] = 'success'
        ret['payload'] = payload
        JsonResponse.__init__(self, data=ret, safe=False)


def generate_page(items, page_number, num_items_per_page, handler):  #items must be an ORM object list
    paginator = Paginator(items, num_items_per_page)
    ret={}
    ret['totalPageCount'] = paginator.num_pages
    ret['totalItemCount'] = items.count()
    page_number = int(page_number)
    if page_number < 1:
        items = paginator.page(1).object_list
    elif page_number > paginator.num_pages:
        items = paginator.page(paginator.num_pages).object_list
    else:
        items = paginator.page(page_number).object_list
    ret['items']=[]
    for item in items:
        ret['items'].append(handler(item))
    return ret

def my_serializer(items, handler):
    ret = []
    for item in items:
        ret.append(handler(item))
    return ret

def underscore_to_camelcase(word):
    return word.split('_')[0] + ''.join(x.capitalize() or '_' for x in word.split('_')[1:])

def model_to_camel_dict(instance, fields=None, exclude=None):
    """
    Return a dict containing the data in ``instance`` suitable for passing as
    a Form's ``initial`` keyword argument.

    ``fields`` is an optional list of field names. If provided, return only the
    named.

    ``exclude`` is an optional list of field names. If provided, exclude the
    named from the returned dict, even if they are listed in the ``fields``
    argument.

    Suggested not included fields: enumerate, foreign key, datetime, many to many
    """
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        if not getattr(f, 'editable', False):
            continue
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        data[underscore_to_camelcase(f.name)] = f.value_from_object(instance)
    return data

def datetime_to_js_timestamp(datetime):
    return int(datetime.timestamp() * 1000)

def get_this_monday():
    # return the date object which is the nearest passed Monday
    return datetime.date.today() - datetime.timedelta(days=datetime.date.isoweekday(datetime.date.today()) - 1)

