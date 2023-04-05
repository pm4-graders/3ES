import json


def serialize(obj):
    """
    Serialize an object @obj into a JSON string
    """
    return json.dumps(obj)


def deserialize(data):
    """
    Deserialize a JSON string @data into an object
    """
    return json.loads(data)
