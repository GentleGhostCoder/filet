# from builtins import bytearray
import collections.abc
import copy
import logging
from typing import Union

from filet.core.json.utils import exists_in_items, get_type
from filet.core.type_mapping import JsonType
from filet.cpputils import JsonHandler

logger = logging.getLogger(__name__)


def set_type(json_type):
    def callback(self, *args, **kwargs):
        current_type, current_schema_ptr, current_prefix, current_key, index = self.schema_ptr_stack[-1]

        if current_key:
            existing_field = next(
                (obj for obj in current_schema_ptr if isinstance(obj, dict) and obj.get("name") == current_key),
                None,
            )
            if existing_field:
                if existing_field["type"] != json_type:
                    if not isinstance(existing_field["type"], list):
                        existing_field["type"] = [existing_field["type"]]
                    if json_type not in existing_field["type"] and isinstance(json_type, list):
                        existing_field["type"].append(json_type)
            else:
                current_schema_ptr.append({"name": f"{current_key}", "type": json_type})
        else:
            if json_type not in current_schema_ptr:
                current_schema_ptr.append(json_type)

        return True

    return callback


class PyAvroSchemaHandler(JsonHandler):  # noqa: C901
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Initialize the base class
        self.schema_exists = False
        self.schema = []  # Root schema
        self.schema_ptr_stack = [
            (JsonType.record, self.schema, "", "root", 0)
        ]  # Stack to track the schema pointer and keys

    @staticmethod
    def create_prefix(prefix, key):
        return f"{prefix}_{key or ''}" if prefix else key

    def reset_schema(self):
        self.schema: list = []
        self.schema_ptr_stack = []
        self.schema_ptr_stack.append((JsonType.record, self.schema, None, "root", 0))

    def update_schema(self, new_schema):
        if not self.schema_exists:
            self.reset_schema()
            self.schema = new_schema
            self.schema_exists = True
            return

        schema_list = [self.schema, new_schema]
        self.create_union_types(schema_list)
        if isinstance(schema_list[0], list) and len(schema_list[0]) == 1:
            self.schema = schema_list[0]

        return self.schema

    def read_existing_schema(self, schema):
        self.reset_schema()
        self.schema = schema
        self.schema_exists = True
        return True

    def create_schema(self, data):
        if not self.schema_exists:
            try:
                self.parse(data)
                # TODO: Check if this is necessary -> currently it fixes the last not unionized schema
                self.update_schema(self.schema)
            except Exception as e:
                logger.error("Error parsing JSON data: %s", e)
                self.schema_exists = False
                return None
            self.schema_exists = True
            return self.schema

        old_schema = copy.deepcopy(self.schema)
        self.reset_schema()
        self.parse(data)
        self.schema_exists = True
        self.update_schema(old_schema)
        return self.schema

    def parse(self, data):
        starts_with_array = False
        if isinstance(data, str):
            data = data.encode("utf-8")
        if data.startswith(b"["):
            starts_with_array = True
            new_data = bytearray(b'{"ArrayWrapper":')
            new_data.extend(data)
            new_data.extend(b"}")
            data = new_data
        is_valid = self.parse_json_bytes(data)
        if not is_valid:
            self.create_union_types(self.schema[0]["type"]["fields"])  # type: ignore
        if starts_with_array:
            self.schema = self.schema[0]["type"]["fields"][-1]["type"]  # type: ignore
        else:
            self.schema = self.schema[0]["type"]
        if "name" not in self.schema:
            self.schema["name"] = "root"  # type: ignore
        self.update_schema(self.schema)
        return is_valid

    String = set_type("string")
    Int = set_type("int")
    Uint = set_type("int")
    Double = set_type("double")
    Int64 = set_type("int")
    Uint64 = set_type("int")
    Null = set_type("null")
    Bool = set_type("boolean")
    RawNumber = set_type("int")

    def Key(self, key, length, copy):
        current_type, current_schema_ptr, current_prefix, current_key, index = self.schema_ptr_stack[-1]
        self.schema_ptr_stack[-1] = (
            current_type,
            current_schema_ptr,
            current_prefix,
            key,
            index,
        )  # Update the current key
        return True

    def StartArray(self):
        new_array = {"type": "array", "items": []}
        current_type, current_schema_ptr, current_prefix, current_key, index = self.schema_ptr_stack[-1]
        index += 1
        if current_key:
            # If we are within an object, append a new field
            current_schema_ptr.append({"name": current_key, "type": new_array})
        else:
            # If we are within an array, directly append the array schema
            current_schema_ptr.append(new_array)

        new_key = self.create_prefix(current_prefix, current_key)
        # Push the new array onto the stack
        self.schema_ptr_stack.append((JsonType.array, new_array["items"], new_key, "", 0))
        return True

    def StartObject(self):
        new_object = {"type": "record", "fields": []}
        current_type, current_schema_ptr, current_prefix, current_key, index = self.schema_ptr_stack[-1]
        index += 1
        new_key = self.create_prefix(current_prefix, current_key)
        new_object["name"] = new_key
        if current_type == JsonType.array:
            # If we are within an array, directly append the record schema
            self.create_union_types(current_schema_ptr)
        # existing_field = next(
        #     (obj for obj in current_schema_ptr if isinstance(obj, dict) and obj.get("name") == new_key), None
        # )
        # if existing_field:
        #     new_object = existing_field
        if current_key:
            # check if the current key object exists in the schema
            current_schema_ptr.append({"name": current_key, "type": new_object})
        else:
            current_schema_ptr.append(new_object)

        self.schema_ptr_stack.append((JsonType.record, new_object["fields"], new_key, "", 0))
        return True

    def EndObject(self, _):
        # compare the types of all items in the array and simplify if possible
        self.schema_ptr_stack.pop()  # Pop the array from the stack
        current_type, current_schema_ptr, current_prefix, current_key, index = self.schema_ptr_stack[-1]
        if current_type == JsonType.array:
            self.create_union_types(current_schema_ptr)
        return True

    def EndArray(self, _):
        # Simplify array items into a single element if possible and handle unions
        current_type, current_schema_ptr, current_prefix, current_key, index = self.schema_ptr_stack[-1]
        self.schema_ptr_stack.pop()  # Pop the array from the stack
        parent_type, parent_schema_ptr, parent_prefix, parent_key, parent_index = self.schema_ptr_stack[-1]
        # compare the types of all items in the array and simplify if possible
        self.create_union_types(current_schema_ptr)
        if parent_type == JsonType.record:
            if (
                len(current_schema_ptr) == 1
                and isinstance(current_schema_ptr[0], dict)
                and current_schema_ptr[0].get("type") == "array"
            ):
                # reduce the array to union of nested array
                parent_schema_ptr[-1]["type"] = {
                    "items": {"items": current_schema_ptr[0]["items"], "type": "array"},
                    "type": "array",
                }
        return True

    def create_union_types(self, current_schema_ptr):  # noqa: C901
        # Create a union type if there are multiple types
        union_types = {}
        types = set()
        for item in current_schema_ptr:
            name, json_type = get_type(item)
            types.add(json_type)

            if not name:
                name = json_type

            if name not in union_types:
                union_types[name] = item
                continue

            previous_name, previous_type = get_type(union_types[name])

            if (
                json_type != previous_type
                and json_type not in [JsonType.array, JsonType.record, JsonType.union]
                and previous_type not in [JsonType.array, JsonType.record, JsonType.union]
            ):
                # create a union type
                if isinstance(union_types[name]["type"], str):
                    union_types[name]["type"] = [previous_type.value, json_type.value]  # type: ignore
                    continue
                if isinstance(union_types[name]["type"], list):
                    if json_type not in union_types[name]["type"]:
                        union_types[name]["type"].append(json_type.value)  # type: ignore
                    continue

            if json_type == JsonType.record and previous_type == JsonType.record:
                # set forward compatibility for record fields
                previous_fields = (
                    union_types[name]["type"]["fields"]
                    if isinstance(union_types[name]["type"], dict)
                    else union_types[name]["fields"]
                )
                current_fields = item["type"]["fields"] if isinstance(item["type"], dict) else item["fields"]
                self.set_compatibility(previous_fields, current_fields)
                self.set_compatibility(current_fields, previous_fields)

            if json_type == JsonType.union and previous_type == JsonType.record:
                # set forward compatibility for record fields
                previous_fields = (
                    union_types[name]["type"]["fields"]
                    if isinstance(union_types[name]["type"], dict)
                    else union_types[name]["fields"]
                )
                for union_item in item["type"]:
                    current_fields = (
                        union_item
                        if isinstance(union_item, str)
                        else (
                            union_item["fields"]
                            if isinstance(union_item, dict)
                            else union_item["type"]["fields"] if isinstance(union_item["type"], dict) else union_item
                        )
                    )
                    if isinstance(union_item, dict):
                        self.set_compatibility(previous_fields, current_fields)
                        self.set_compatibility(current_fields, previous_fields)

            if json_type == JsonType.record and previous_type == JsonType.union:
                # set forward compatibility for record fields
                current_fields = item["type"]["fields"] if isinstance(item["type"], dict) else item["fields"]
                for union_item in union_types[name]["type"]:
                    previous_fields = (
                        union_item
                        if isinstance(union_item, str)
                        else (
                            union_item["fields"]
                            if isinstance(union_item, dict)
                            else union_item["type"]["fields"] if isinstance(union_item["type"], dict) else union_item
                        )
                    )
                    if isinstance(union_item, dict):
                        self.set_compatibility(previous_fields, current_fields)
                        self.set_compatibility(current_fields, previous_fields)

            if json_type == JsonType.union and previous_type == JsonType.union:
                new_type = [*union_types[name]["type"], *item["type"]]
                self.create_union_types(new_type)
                union_types[name]["type"] = new_type  # type: ignore
                continue

            if json_type == JsonType.array:
                # make the items of the array to be a union of the items
                if "items" in item:
                    if isinstance(item["items"], list):
                        self.create_union_types(item["items"])
                    elif isinstance(union_types[name]["items"], dict) and isinstance(item["items"], dict):
                        self.recursive_update(union_types[name]["items"], item["items"], True)

            if json_type in [JsonType.array, JsonType.record]:
                self.recursive_update(union_types[name], item, True)

        union_schema = []

        for name, item in union_types.items():
            if name in ["record", "array", "union"] and not item:
                continue
            union_schema.append(item)

        current_schema_ptr.clear()
        current_schema_ptr.extend(union_schema)

    @staticmethod
    def set_compatibility(items1, items2):
        new_items = []

        for item in items1:
            new_items.append(item)
            # Backward compatibility
            if not exists_in_items(items2, item):
                # Assuming item is a dictionary (JsonMap equivalent in Python)
                item["default"] = None

                if isinstance(item["type"], dict) or isinstance(item["type"], str):
                    item["type"] = ["null", item["type"]]
                    new_items.append(item)
                    continue

                if isinstance(item["type"], list):
                    null_exists = any(type_item == "null" for type_item in item["type"])
                    if not null_exists:
                        item["type"].append("null")
                    continue

        # Updating items1 directly to reflect changes
        items1.clear()
        items1.extend(new_items)

    def recursive_update(self, d, u, merge_lists=False):
        """Method to recursively update a dictionary."""
        if isinstance(d, collections.abc.Mapping):
            for k, v in u.items():
                if isinstance(v, collections.abc.Mapping):
                    d[k] = self.recursive_update(d.get(k, {}), v, merge_lists)
                elif merge_lists and isinstance(v, list) and isinstance(d.get(k), list):
                    d[k].extend(v)
                    self.create_union_types(d[k])
                else:
                    d[k] = v
        elif isinstance(d, list):
            d.append(u)
            self.create_union_types(d)
        return d


def eval_json(data: Union[bytes, str]) -> dict:
    """Evaluate JSON data to generate an Avro schema.

    If the JSON data represents a list, it is wrapped in a dictionary
    to ensure compatibility with certain data processing frameworks.

    :param data: The JSON data to be evaluated. This can be either a bytes object or a string.
    :return: A dictionary representing the Avro schema generated from the JSON data.

    Example:

    >>> json_data = '[{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]'
    >>> schema = eval_json(json_data)
    >>> print(schema['type'])
    record
    >>> print(schema['fields'][0]['name'])
    root
    """
    schema = PyAvroSchemaHandler().create_schema(data)
    if (isinstance(data, str) and data.startswith("[")) or (isinstance(data, bytes) and data.startswith(b"[")):
        logger.debug(
            "JSON data is an ARRAY. Wrapping it in a dictionary "
            "to ensure compatibility with certain data processing frameworks."
        )
        schema = {"name": "rootArrayWrapper", "type": "record", "fields": [{"name": "root", "type": schema}]}

    return schema  # type: ignore
