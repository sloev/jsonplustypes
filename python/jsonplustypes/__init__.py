import datetime, time
import json


### DEFAULTS ###
def encode_datetime(date_object):
    timestamp = int(1000 * time.mktime(date_object.utctimetuple()))
    return {
            _TYPE_TAG:"DATETIME",
            _VALUE_TAG:timestamp
        }

def decode_datetime(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp/1000)

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
    """Convertsi
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
        JSONDecoder.__init__(self, object_hook=self.dict_to_object, *args, **kwargs)

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
