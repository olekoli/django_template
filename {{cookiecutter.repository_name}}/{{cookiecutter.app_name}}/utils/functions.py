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
