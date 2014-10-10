JSON plus types
***************

Uses builtin json. but adds a lookup dictionary with functions that encode/decode specific types.

default _TYPE_FUNCS dict holds:

_TYPE_FUNCS{
datetime.datetime: encode_datetime,
"DATETIME": decode_datetime,
float:encode_float
}

where encode ande decode datetime functions:

def encode_datetime(date_object):
    timestamp = int(1000 * time.mktime(date_object.utctimetuple()))
    return {
            _TYPE_TAG:"DATETIME",
            _VALUE_TAG:timestamp
        }

def decode_datetime(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp/1000)

the github repo:
http://github.com/sloev/jsonplustypes
holds a reference javascript implementation of the same json serialization/deserialization


