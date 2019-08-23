from typing import Any, Dict, List

from django.db.models import Model


def deep_get(dictionary: Dict, path: str, default: str = None) -> Any:
    keys = path.split("/")
    val = None

    for key in keys:
        if val:
            if isinstance(val, list):
                val = [v.get(key, default) if v else None for v in val]
            else:
                val = val.get(key, default)
        else:
            val = dictionary.get(key, default)

        if not val:
            break
    return val


def update_instance(instance: Model, args: Dict, exception: List = ["id"]) -> Model:
    if instance:
        [
            setattr(instance, key, value)
            for key, value in args.items()
            if key not in exception
        ]
    instance.save()
    return instance


def dict_to_camel_case(input_dict: Dict) -> Dict:
    """
    Converts all keys in the dictionary from snake_case to camelCase to simplify making graphql queries
    :param input_dict: Any valid dictionary
    :return: Returns a dictionary with all of the keys in camelCase
    """

    def variable_to_camel_case(variable: str) -> str:
        parts = variable.split("_")
        return "".join(
            list(map(lambda x: x.capitalize() if parts.index(x) != 0 else x, parts))
        )

    new_dict = {}

    for k, v in input_dict.items():
        if isinstance(v, dict):
            v = dict_to_camel_case(v)
        new_dict[variable_to_camel_case(k)] = v

    return new_dict
