import datetime, time
import json

_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


### DEFAULTS ###
def encode_datetime(date_object):
    date_string = datetime.datetime.strftime(date_object, _DATE_FORMAT)
    return {
            _TYPE_TAG:"DATETIME",
            _VALUE_TAG:date_string
        }

def decode_datetime(date_string):
    return datetime.datetime.strptime(date_string, _DATE_FORMAT)

def encode_float(obj):
    return format(obj, ".2f")

_TYPE_FUNCS = {
    'DATETIME':decode_datetime,
    datetime.datetime:encode_datetime,
    float:encode_float
}
### END DEFAULTS ###


### STATIC ###
_TYPE_TAG = u'__TYPE__'
_VALUE_TAG = u'__VALUE__'
### END STATIC ###


class __JSONEncoder(json.JSONEncoder):
    """Converts
    Converts a python object, where datetime and timedelta objects are converted
    into objects that can be decoded using the DateTimeAwareJSONDecoder.
    """
    def default(self, obj):
        if isinstance(obj, basestring):
            return obj
        try:
            func = _TYPE_FUNCS[ type(obj) ]
            return func(obj)
        except KeyError, e:
            return JSONEncoder.default(self, obj)

class __JSONDecoder(json.JSONDecoder):
    """
    Converts a json string, where datetime and timedelta objects were converted
    into objects using the DateTimeAwareJSONEncoder, back into a python object.
    """
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object, *args, **kwargs)

    def dict_to_object(self, d):
        try:
            func = _TYPE_FUNCS[ d[ _TYPE_TAG ] ]
            value = d[ _VALUE_TAG ]
            return func(value)
        except KeyError, e:
            return d

### PUBLIC METHODS ###

def dumps(data):
    return json.dumps(data, cls=__JSONEncoder)

def loads(data):
    return json.loads(data, cls=__JSONDecoder)

def add_lookup(key, value):
    _TYPE_FUNCS[key] = value

def del_lookup(key):
    _TYPE_FUNCS.pop(key)
