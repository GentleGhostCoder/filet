from typing import Tuple

from filet.core.type_mapping import JsonType


def get_type(item) -> Tuple[str, JsonType]:
    if isinstance(item, str):
        return "", JsonType(item)
    name = ""
    json_type = "string"
    if isinstance(item, dict):
        if "name" in item:
            if isinstance(item["name"], str):
                name = item["name"]
        if "type" in item:
            if isinstance(item["type"], str):
                json_type = item["type"]
            if isinstance(item["type"], list):
                json_type = "union"
            if isinstance(item["type"], dict) and "type" in item["type"]:
                json_type = item["type"]["type"]
    return name, JsonType(json_type)


def exists_in_items(items, item):
    return any(
        (item == array_item)
        or (isinstance(item, dict) and isinstance(array_item, dict) and item.get("name") == array_item.get("name"))
        for array_item in items
    )
