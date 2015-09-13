import datetime, time
from json import dumps as _dumps
from json import loads as _loads
from json import JSONEncoder, JSONDecoder, encoder
from bson.objectid import ObjectId


old_FLOAT_REPR = encoder.FLOAT_REPR
old_c_make_encoder = encoder.c_make_encoder

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

def encode_date(obj):
    _dtime = datetime.datetime.combine(obj, datetime.datetime.min.time())
    return encode_datetime(_dtime)

_TYPE_FUNCS = {
    'DATETIME':decode_datetime,
    datetime.datetime:encode_datetime,
    datetime.date:encode_date,
    ObjectId:str,
}
### END DEFAULTS ###


### STATIC ###
_TYPE_TAG = u'__TYPE__'
_VALUE_TAG = u'__VALUE__'
### END STATIC ###


class JsonPlusEncoder(JSONEncoder):
    """Converts
    Converts a python object, where datetime and timedelta objects are converted
    into objects that can be decoded using the DateTimeAwareJSONDecoder.
    """
    def default(self, obj):
        try:
            return _TYPE_FUNCS[ type(obj) ](obj)
        except KeyError, e:
            return JSONEncoder.default(self, obj)

class JsonPlusDecoder(JSONDecoder):
    """
    Converts a json string, where datetime and timedelta objects were converted
    into objects using the DateTimeAwareJSONEncoder, back into a python object.
    """
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self, object_hook=self.dict_to_object, *args, **kwargs)

    def dict_to_object(self, d):
        try:
            return _TYPE_FUNCS[d[_TYPE_TAG]](d[_VALUE_TAG])
        except KeyError, e:
            return d

### PUBLIC METHODS ###

def dumps(data, round_digits=False, precision=2):
    if round_digits:
        def float_to_str(f): return '%.*f' % (precision, f)

        encoder.FLOAT_REPR = float_to_str
        encoder.c_make_encoder = None

        return _dumps(data, cls=JsonPlusEncoder)
        #clean ups
        encoder.FLOAT_REPR = old_FLOAT_REPR
        encoder.c_make_encoder = old_c_make_encoder
    else:
        return _dumps(data, cls=JsonPlusEncoder)

def loads(data):
    return _loads(data, cls=JsonPlusDecoder)

def add_lookup(key, value):
    _TYPE_FUNCS[key] = value

def del_lookup(key):
    _TYPE_FUNCS.pop(key)
