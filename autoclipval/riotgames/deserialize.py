import re
import typing

def json_to_python_name(json_name: str) -> str:
    """Returns a snake_case name for a camelCase json field name"""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", json_name).lower()


def unmarshal_dict(data: typing.Dict, t: type) -> t:
    """Unmarshals a dict to an attrs object"""
    for k, v in data.items():
        attr_name = json_to_python_name(k)
        attr_type = t.__annotations__.get(attr_name)
