from io import BytesIO
import json

import avro
from avro.compatibility import ReaderWriterCompatibilityChecker, SchemaCompatibilityType
from avro.datafile import DataFileWriter
from avro.io import DatumWriter

from tests.generate_data import generate_complex_union_json_data

# from filet.cpputils import AvroSchemaHandler
from filet.core.json.avro_schema_handler import PyAvroSchemaHandler as AvroSchemaHandler
from filet.core.json.json_fix_handler import JsonFixHandler


def test_avro_complex_record():
    json_data = generate_complex_union_json_data()
    handler = AvroSchemaHandler()
    handler.parse(json_data)
    schema = handler.schema
    avro_schema = avro.schema.parse(json.dumps(schema))
    writer = DataFileWriter(BytesIO(), DatumWriter(), avro_schema)
    writer.append(json.loads(json_data))
    writer.close()
    assert repr(schema) == repr(
        {
            "type": "record",
            "fields": [
                {"name": "id", "type": "string"},
                {"name": "name", "type": "string"},
                {"name": "isActive", "type": "boolean"},
                {"name": "counts", "type": {"type": "array", "items": ["int", "null"]}},
                {"name": "tags", "type": {"type": "array", "items": ["string", "null"]}},
                {
                    "name": "metadata",
                    "type": {
                        "type": "record",
                        "fields": [
                            {"name": "createdDate", "type": "string"},
                            {"name": "updatedDate", "type": "null"},
                            {
                                "name": "contributors",
                                "type": {
                                    "type": "array",
                                    "items": [
                                        {
                                            "type": "record",
                                            "fields": [
                                                {"name": "name", "type": "string"},
                                                {"name": "roles", "type": {"type": "array", "items": ["string"]}},
                                                {
                                                    "name": "contact",
                                                    "type": {
                                                        "type": "record",
                                                        "fields": [
                                                            {"name": "email", "type": "string"},
                                                            {
                                                                "name": "phoneNumbers",
                                                                "type": {"type": "array", "items": ["string", "null"]},
                                                            },
                                                        ],
                                                        "name": "root_metadata_contributors__contact",
                                                    },
                                                },
                                            ],
                                            "name": "root_metadata_contributors_",
                                        }
                                    ],
                                },
                            },
                        ],
                        "name": "root_metadata",
                    },
                },
                {
                    "name": "relatedObjects",
                    "type": {
                        "type": "array",
                        "items": [
                            {
                                "type": "record",
                                "fields": [
                                    {"name": "id", "type": "string"},
                                    {"name": "type", "type": "string"},
                                    {
                                        "name": "properties",
                                        "type": {
                                            "type": "record",
                                            "fields": [
                                                {"name": "property1", "type": "string"},
                                                {"name": "property2", "type": "int"},
                                                {"name": "property3", "type": "boolean"},
                                                {"name": "property4", "type": "null"},
                                            ],
                                            "name": "root_relatedObjects__properties",
                                        },
                                    },
                                ],
                                "name": "root_relatedObjects_",
                            }
                        ],
                    },
                },
                {"name": "optionalField", "type": "null"},
                {
                    "name": "miscellaneous",
                    "type": {
                        "type": "record",
                        "fields": [
                            {
                                "name": "anyOf",
                                "type": {
                                    "type": "array",
                                    "items": [
                                        {
                                            "type": "record",
                                            "fields": [
                                                {"name": "type", "type": "string"},
                                                {"name": "description", "type": "string"},
                                                {
                                                    "name": "details",
                                                    "type": {
                                                        "type": "record",
                                                        "fields": [{"name": "detail1", "type": "string"}],
                                                        "name": "root_miscellaneous_anyOf__details",
                                                    },
                                                },
                                            ],
                                            "name": "root_miscellaneous_anyOf_",
                                        },
                                        "string",
                                        "int",
                                        "boolean",
                                    ],
                                },
                            }
                        ],
                        "name": "root_miscellaneous",
                    },
                },
                {
                    "name": "numericData",
                    "type": {
                        "type": "record",
                        "fields": [
                            {"name": "integerValue", "type": "int"},
                            {"name": "floatValue", "type": "double"},
                            {"name": "doubleValue", "type": "null"},
                        ],
                        "name": "root_numericData",
                    },
                },
                {
                    "name": "booleanFlags",
                    "type": {
                        "type": "record",
                        "fields": [
                            {"name": "flag1", "type": "boolean"},
                            {"name": "flag2", "type": "boolean"},
                            {"name": "flag3", "type": "null"},
                        ],
                        "name": "root_booleanFlags",
                    },
                },
                {"name": "emptyArray", "type": {"type": "array", "items": ["string"]}},
                {
                    "name": "complexArray",
                    "type": {
                        "items": {
                            "items": [
                                "string",
                                {"type": "array", "items": ["int"]},
                                "int",
                                "null",
                                {
                                    "type": "record",
                                    "fields": [{"name": "key", "type": "string"}],
                                    "name": "root_complexArray__",
                                },
                                "boolean",
                            ],
                            "type": "array",
                        },
                        "type": "array",
                    },
                },
                {
                    "name": "unionType",
                    "type": {
                        "type": "array",
                        "items": [
                            "string",
                            "int",
                            "boolean",
                            "null",
                            {
                                "type": "record",
                                "fields": [{"name": "unionObject", "type": "string"}],
                                "name": "root_unionType_",
                            },
                        ],
                    },
                },
                {
                    "name": "anotherRecord",
                    "type": {
                        "type": "record",
                        "fields": [
                            {"name": "test", "type": {"type": "array", "items": ["int"]}},
                            {
                                "name": "user",
                                "type": {
                                    "type": "record",
                                    "fields": [
                                        {"name": "name", "type": "string"},
                                        {"name": "age", "type": "int"},
                                        {"name": "emails", "type": {"type": "array", "items": ["string"]}},
                                        {
                                            "name": "address",
                                            "type": {
                                                "type": "record",
                                                "fields": [
                                                    {"name": "street", "type": "string"},
                                                    {"name": "city", "type": "string"},
                                                    {"name": "zipCode", "type": "string"},
                                                ],
                                                "name": "root_anotherRecord_user_address",
                                            },
                                        },
                                    ],
                                    "name": "root_anotherRecord_user",
                                },
                            },
                            {
                                "name": "products",
                                "type": {
                                    "type": "array",
                                    "items": [
                                        {
                                            "type": "record",
                                            "fields": [
                                                {"name": "id", "type": "int"},
                                                {"name": "name", "type": "string"},
                                                {
                                                    "name": "tags",
                                                    "type": {"type": "array", "items": ["string", "null"]},
                                                },
                                                {
                                                    "name": "flags",
                                                    "type": [
                                                        "null",
                                                        {
                                                            "type": "record",
                                                            "fields": [
                                                                {"name": "flag1", "type": "boolean"},
                                                                {"name": "flag2", "type": "boolean"},
                                                            ],
                                                            "name": "root_anotherRecord_products__flags",
                                                        },
                                                    ],
                                                    "default": None,
                                                },
                                            ],
                                            "name": "root_anotherRecord_products_",
                                        }
                                    ],
                                },
                            },
                        ],
                        "name": "root_anotherRecord",
                    },
                },
                {
                    "name": "prometheus",
                    "type": {
                        "type": "record",
                        "fields": [
                            {"name": "status", "type": "string"},
                            {
                                "name": "data",
                                "type": {
                                    "type": "record",
                                    "fields": [
                                        {"name": "resultType", "type": "string"},
                                        {
                                            "name": "result",
                                            "type": {
                                                "type": "array",
                                                "items": [
                                                    {
                                                        "type": "record",
                                                        "fields": [
                                                            {
                                                                "name": "metric",
                                                                "type": {
                                                                    "type": "record",
                                                                    "fields": [
                                                                        {"name": "__name__", "type": "string"},
                                                                        {
                                                                            "name": "test",
                                                                            "type": ["null", "string"],
                                                                            "default": None,
                                                                        },
                                                                        {
                                                                            "name": "alias",
                                                                            "type": ["null", "string"],
                                                                            "default": None,
                                                                        },
                                                                        {
                                                                            "name": "cluster",
                                                                            "type": ["null", "string"],
                                                                            "default": None,
                                                                        },
                                                                        {
                                                                            "name": "datacenter",
                                                                            "type": ["null", "string"],
                                                                            "default": None,
                                                                        },
                                                                        {"name": "instance", "type": "string"},
                                                                        {
                                                                            "name": "job",
                                                                            "type": ["null", "string"],
                                                                            "default": None,
                                                                        },
                                                                        {
                                                                            "name": "recordings",
                                                                            "type": ["null", "string"],
                                                                            "default": None,
                                                                        },
                                                                        {
                                                                            "name": "cpu",
                                                                            "type": ["null", "string"],
                                                                            "default": None,
                                                                        },
                                                                        {
                                                                            "name": "mode",
                                                                            "type": ["null", "string"],
                                                                            "default": None,
                                                                        },
                                                                        {
                                                                            "name": "type",
                                                                            "type": ["null", "string"],
                                                                            "default": None,
                                                                        },
                                                                    ],
                                                                    "name": "root_prometheus_data_result__metric",
                                                                },
                                                            },
                                                            {
                                                                "name": "values",
                                                                "type": {
                                                                    "items": {
                                                                        "items": ["int", "string"],
                                                                        "type": "array",
                                                                    },
                                                                    "type": "array",
                                                                },
                                                            },
                                                        ],
                                                        "name": "root_prometheus_data_result_",
                                                    }
                                                ],
                                            },
                                        },
                                    ],
                                    "name": "root_prometheus_data",
                                },
                            },
                        ],
                        "name": "root_prometheus",
                    },
                },
            ],
            "name": "root",
        }
    )


def test_avro_complex_array():
    json_data = "[" + generate_complex_union_json_data() + "]"
    handler = AvroSchemaHandler()
    handler.parse(json_data)
    schema = handler.schema
    avro_schema = avro.schema.parse(json.dumps(schema))
    writer = DataFileWriter(BytesIO(), DatumWriter(), avro_schema)
    writer.append(json.loads(json_data))
    writer.close()
    assert repr(schema) == repr(
        {
            "type": "array",
            "items": [
                {
                    "type": "record",
                    "fields": [
                        {"name": "id", "type": "string"},
                        {"name": "name", "type": "string"},
                        {"name": "isActive", "type": "boolean"},
                        {"name": "counts", "type": {"type": "array", "items": ["int", "null"]}},
                        {"name": "tags", "type": {"type": "array", "items": ["string", "null"]}},
                        {
                            "name": "metadata",
                            "type": {
                                "type": "record",
                                "fields": [
                                    {"name": "createdDate", "type": "string"},
                                    {"name": "updatedDate", "type": "null"},
                                    {
                                        "name": "contributors",
                                        "type": {
                                            "type": "array",
                                            "items": [
                                                {
                                                    "type": "record",
                                                    "fields": [
                                                        {"name": "name", "type": "string"},
                                                        {
                                                            "name": "roles",
                                                            "type": {"type": "array", "items": ["string"]},
                                                        },
                                                        {
                                                            "name": "contact",
                                                            "type": {
                                                                "type": "record",
                                                                "fields": [
                                                                    {"name": "email", "type": "string"},
                                                                    {
                                                                        "name": "phoneNumbers",
                                                                        "type": {
                                                                            "type": "array",
                                                                            "items": ["string", "null"],
                                                                        },
                                                                    },
                                                                ],
                                                                "name": "root_ArrayWrapper__metadata_contributors__contact",
                                                            },
                                                        },
                                                    ],
                                                    "name": "root_ArrayWrapper__metadata_contributors_",
                                                }
                                            ],
                                        },
                                    },
                                ],
                                "name": "root_ArrayWrapper__metadata",
                            },
                        },
                        {
                            "name": "relatedObjects",
                            "type": {
                                "type": "array",
                                "items": [
                                    {
                                        "type": "record",
                                        "fields": [
                                            {"name": "id", "type": "string"},
                                            {"name": "type", "type": "string"},
                                            {
                                                "name": "properties",
                                                "type": {
                                                    "type": "record",
                                                    "fields": [
                                                        {"name": "property1", "type": "string"},
                                                        {"name": "property2", "type": "int"},
                                                        {"name": "property3", "type": "boolean"},
                                                        {"name": "property4", "type": "null"},
                                                    ],
                                                    "name": "root_ArrayWrapper__relatedObjects__properties",
                                                },
                                            },
                                        ],
                                        "name": "root_ArrayWrapper__relatedObjects_",
                                    }
                                ],
                            },
                        },
                        {"name": "optionalField", "type": "null"},
                        {
                            "name": "miscellaneous",
                            "type": {
                                "type": "record",
                                "fields": [
                                    {
                                        "name": "anyOf",
                                        "type": {
                                            "type": "array",
                                            "items": [
                                                {
                                                    "type": "record",
                                                    "fields": [
                                                        {"name": "type", "type": "string"},
                                                        {"name": "description", "type": "string"},
                                                        {
                                                            "name": "details",
                                                            "type": {
                                                                "type": "record",
                                                                "fields": [{"name": "detail1", "type": "string"}],
                                                                "name": "root_ArrayWrapper__miscellaneous_anyOf__details",
                                                            },
                                                        },
                                                    ],
                                                    "name": "root_ArrayWrapper__miscellaneous_anyOf_",
                                                },
                                                "string",
                                                "int",
                                                "boolean",
                                            ],
                                        },
                                    }
                                ],
                                "name": "root_ArrayWrapper__miscellaneous",
                            },
                        },
                        {
                            "name": "numericData",
                            "type": {
                                "type": "record",
                                "fields": [
                                    {"name": "integerValue", "type": "int"},
                                    {"name": "floatValue", "type": "double"},
                                    {"name": "doubleValue", "type": "null"},
                                ],
                                "name": "root_ArrayWrapper__numericData",
                            },
                        },
                        {
                            "name": "booleanFlags",
                            "type": {
                                "type": "record",
                                "fields": [
                                    {"name": "flag1", "type": "boolean"},
                                    {"name": "flag2", "type": "boolean"},
                                    {"name": "flag3", "type": "null"},
                                ],
                                "name": "root_ArrayWrapper__booleanFlags",
                            },
                        },
                        {"name": "emptyArray", "type": {"type": "array", "items": ["string"]}},
                        {
                            "name": "complexArray",
                            "type": {
                                "items": {
                                    "items": [
                                        "string",
                                        {"type": "array", "items": ["int"]},
                                        "int",
                                        "null",
                                        {
                                            "type": "record",
                                            "fields": [{"name": "key", "type": "string"}],
                                            "name": "root_ArrayWrapper__complexArray__",
                                        },
                                        "boolean",
                                    ],
                                    "type": "array",
                                },
                                "type": "array",
                            },
                        },
                        {
                            "name": "unionType",
                            "type": {
                                "type": "array",
                                "items": [
                                    "string",
                                    "int",
                                    "boolean",
                                    "null",
                                    {
                                        "type": "record",
                                        "fields": [{"name": "unionObject", "type": "string"}],
                                        "name": "root_ArrayWrapper__unionType_",
                                    },
                                ],
                            },
                        },
                        {
                            "name": "anotherRecord",
                            "type": {
                                "type": "record",
                                "fields": [
                                    {"name": "test", "type": {"type": "array", "items": ["int"]}},
                                    {
                                        "name": "user",
                                        "type": {
                                            "type": "record",
                                            "fields": [
                                                {"name": "name", "type": "string"},
                                                {"name": "age", "type": "int"},
                                                {"name": "emails", "type": {"type": "array", "items": ["string"]}},
                                                {
                                                    "name": "address",
                                                    "type": {
                                                        "type": "record",
                                                        "fields": [
                                                            {"name": "street", "type": "string"},
                                                            {"name": "city", "type": "string"},
                                                            {"name": "zipCode", "type": "string"},
                                                        ],
                                                        "name": "root_ArrayWrapper__anotherRecord_user_address",
                                                    },
                                                },
                                            ],
                                            "name": "root_ArrayWrapper__anotherRecord_user",
                                        },
                                    },
                                    {
                                        "name": "products",
                                        "type": {
                                            "type": "array",
                                            "items": [
                                                {
                                                    "type": "record",
                                                    "fields": [
                                                        {"name": "id", "type": "int"},
                                                        {"name": "name", "type": "string"},
                                                        {
                                                            "name": "tags",
                                                            "type": {"type": "array", "items": ["string", "null"]},
                                                        },
                                                        {
                                                            "name": "flags",
                                                            "type": [
                                                                "null",
                                                                {
                                                                    "type": "record",
                                                                    "fields": [
                                                                        {"name": "flag1", "type": "boolean"},
                                                                        {"name": "flag2", "type": "boolean"},
                                                                    ],
                                                                    "name": "root_ArrayWrapper__anotherRecord_products__flags",
                                                                },
                                                            ],
                                                            "default": None,
                                                        },
                                                    ],
                                                    "name": "root_ArrayWrapper__anotherRecord_products_",
                                                }
                                            ],
                                        },
                                    },
                                ],
                                "name": "root_ArrayWrapper__anotherRecord",
                            },
                        },
                        {
                            "name": "prometheus",
                            "type": {
                                "type": "record",
                                "fields": [
                                    {"name": "status", "type": "string"},
                                    {
                                        "name": "data",
                                        "type": {
                                            "type": "record",
                                            "fields": [
                                                {"name": "resultType", "type": "string"},
                                                {
                                                    "name": "result",
                                                    "type": {
                                                        "type": "array",
                                                        "items": [
                                                            {
                                                                "type": "record",
                                                                "fields": [
                                                                    {
                                                                        "name": "metric",
                                                                        "type": {
                                                                            "type": "record",
                                                                            "fields": [
                                                                                {"name": "__name__", "type": "string"},
                                                                                {
                                                                                    "name": "test",
                                                                                    "type": ["null", "string"],
                                                                                    "default": None,
                                                                                },
                                                                                {
                                                                                    "name": "alias",
                                                                                    "type": ["null", "string"],
                                                                                    "default": None,
                                                                                },
                                                                                {
                                                                                    "name": "cluster",
                                                                                    "type": ["null", "string"],
                                                                                    "default": None,
                                                                                },
                                                                                {
                                                                                    "name": "datacenter",
                                                                                    "type": ["null", "string"],
                                                                                    "default": None,
                                                                                },
                                                                                {"name": "instance", "type": "string"},
                                                                                {
                                                                                    "name": "job",
                                                                                    "type": ["null", "string"],
                                                                                    "default": None,
                                                                                },
                                                                                {
                                                                                    "name": "recordings",
                                                                                    "type": ["null", "string"],
                                                                                    "default": None,
                                                                                },
                                                                                {
                                                                                    "name": "cpu",
                                                                                    "type": ["null", "string"],
                                                                                    "default": None,
                                                                                },
                                                                                {
                                                                                    "name": "mode",
                                                                                    "type": ["null", "string"],
                                                                                    "default": None,
                                                                                },
                                                                                {
                                                                                    "name": "type",
                                                                                    "type": ["null", "string"],
                                                                                    "default": None,
                                                                                },
                                                                            ],
                                                                            "name": "root_ArrayWrapper__prometheus_data_result__metric",
                                                                        },
                                                                    },
                                                                    {
                                                                        "name": "values",
                                                                        "type": {
                                                                            "items": {
                                                                                "items": ["int", "string"],
                                                                                "type": "array",
                                                                            },
                                                                            "type": "array",
                                                                        },
                                                                    },
                                                                ],
                                                                "name": "root_ArrayWrapper__prometheus_data_result_",
                                                            }
                                                        ],
                                                    },
                                                },
                                            ],
                                            "name": "root_ArrayWrapper__prometheus_data",
                                        },
                                    },
                                ],
                                "name": "root_ArrayWrapper__prometheus",
                            },
                        },
                    ],
                    "name": "root_ArrayWrapper_",
                }
            ],
            "name": "root",
        }
    )


def test_avro_schema_evolute():
    json_data1 = """
    {
      "userId": "user123",
      "email": "user123@example.com",
      "age": 30
    }
    """
    json_data2 = """
    {
      "userId": "user456",
      "username": "new_user",
      "age": "thirty-one"
    }
    """
    handler = AvroSchemaHandler()
    schema = handler.create_schema(json_data1)
    updated_schema = handler.create_schema(json_data2)
    avro_schema = avro.schema.parse(json.dumps(schema))
    updated_avro_schema = avro.schema.parse(json.dumps(updated_schema))
    compatibility = ReaderWriterCompatibilityChecker().get_compatibility(reader=updated_avro_schema, writer=avro_schema)
    assert compatibility.compatibility == SchemaCompatibilityType.compatible
    writer = DataFileWriter(BytesIO(), DatumWriter(), updated_avro_schema)
    writer.append(json.loads(json_data1))
    writer.append(json.loads(json_data2))
    writer.close()


def test_read_existing_avro_schema():
    handler = AvroSchemaHandler()
    assert handler.read_existing_schema(
        {
            "type": "record",
            "name": "UserProfile",
            "fields": [
                {"name": "userId", "type": "string"},
                {"name": "email", "type": "string"},
                {"name": "age", "type": "int"},
            ],
        }
    )
    avro_schema = avro.schema.parse(json.dumps(handler.schema))
    handler.update_schema(
        {
            "type": "record",
            "name": "UserProfile",
            "fields": [
                {"name": "userId", "type": "string"},
                {"name": "age", "type": "string"},
                {"name": "username", "type": "string"},
            ],
        }
    )
    updated_avro_schema = avro.schema.parse(json.dumps(handler.schema))
    # ForwardCompatible
    compatibility = ReaderWriterCompatibilityChecker().get_compatibility(reader=updated_avro_schema, writer=avro_schema)
    assert compatibility.compatibility == SchemaCompatibilityType.compatible
    json_data1 = """
    {
      "userId": "user123",
      "email": "user123@example.com",
      "age": 30
    }
    """
    json_data2 = """
    {
      "userId": "user456",
      "username": "new_user",
      "age": "thirty-one"
    }
    """
    writer = DataFileWriter(BytesIO(), DatumWriter(), updated_avro_schema)
    writer.append(json.loads(json_data1))
    writer.append(json.loads(json_data2))
    writer.close()


def test_nested_prometheus_json():
    test_json = """
    {
    "status": "success",
    "data": {
    "resultType": "matrix",
    "result": [
            {
            "metric": {
              "__name__": "node_memory_MemTotal_bytes",
              "alias": "datacenteraggregation",
              "cluster": "F1C20",
              "datacenter": "de-kae-bs-kvm-live",
              "instance": "onode012035.server.lan:9100",
              "job": "clusters"
            },
            "values": [
              [
                1698678900,
                "809772896256"
              ],
              [
                1698678960,
                "809772896256"
              ],
              [
                1698679020,
                "809772896256"
              ],
              [
                1698679080,
                "809772896256"
              ],
              [
                1698679140,
                "809772896256"
              ],
              [
                1698679200,
                "809772896256"
              ]
            ]
          },
          {
            "metric": {
              "__name__": "node_memory_MemTotal_bytes",
              "alias": "datacenteraggregation",
              "cluster": "F1C3",
              "datacenter": "de-kae-bs-esxi-live",
              "instance": "localhost:9100",
              "job": "self",
              "recordings": "clusters"
            },
            "values": [
              [
                1698678900,
                "6216773632"
              ],
              [
                1698678960,
                "6216773632"
              ],
              [
                1698679020,
                "6216773632"
              ],
              [
                1698679080,
                "6216773632"
              ],
              [
                1698679140,
                "6216773632"
              ],
              [
                1698679200,
                "6216773632"
              ]
            ]
         },
          {
            "metric": {
              "__name__": "node_memory_MemTotal_bytes",
              "alias": "datacenteraggregation",
              "cluster": "F1C3",
              "datacenter": "de-kae-bs-esxi-live",
              "instance": "localhost:9100",
              "job": "self",
              "recordings": "clusters"
            },
            "values": [
              [
                1698678900,
                "6216773632"
              ],
              [
                1698678960,
                "6216773632"
              ],
              [
                1698679020,
                "6216773632"
              ],
              [
                1698679080,
                "6216773632"
              ],
              [
                1698679140,
                "6216773632"
              ],
              [
                1698679200,
                "6216773632"
              ]
            ]
         },
          {
            "metric": {
              "__name__": "node_memory_MemTotal_bytes",
              "alias": "datacenteraggregation",
              "cluster": "F1C3",
              "datacenter": "de-kae-bs-esxi-live",
              "instance": "localhost:9100"
            },
            "values": [
              [
                1698678900,
                "6216773632"
              ],
              [
                1698678960,
                "6216773632"
              ],
              [
                1698679020,
                "6216773632"
              ],
              [
                1698679080,
                "6216773632"
              ],
              [
                1698679140,
                "6216773632"
              ],
              [
                1698679200,
                "6216773632"
              ]
            ]
         }
        ]
      }
    }
    """
    handler = AvroSchemaHandler()
    schema = handler.create_schema(test_json)
    avro_schema = avro.schema.parse(json.dumps(schema))
    writer = DataFileWriter(BytesIO(), DatumWriter(), avro_schema)
    writer.append(json.loads(test_json))
    writer.close()


def test_incomplete_json():
    test_json = '{"status":"success","data":{"resultType":"matrix","result":[{"metric":{"__name__":"node_memory_MemTotal_bytes","alias":"datacenteraggregation","cluster":"F10C1","datacenter":"us-mkc-ga-kvm-live","instance":"onode100101.server.lan:9100","job":"clusters"},"values":[[1698674400,"403904868352"],[1698674460,"403904868352"],[1698674520,"403904868352"],[1698674580,"403904868352"],[1698674640,"403904868352"],[1698674700,"403904868352"]]},{"metric":{"__name__":"node_memory_MemTotal_bytes","alias":"datacenteraggregation","cluster":"F10C1","datacenter":"us-mkc-ga-kvm-live","instance":"onode100102.server.lan:9100","job":"clusters"},"values":[[1698674400,"404039708672"],[1698674460,"404039708672"],[1698674520,"404039708672"],[1698674580,"404039708672"],[1698674640,"404039708672"],[1698674700,"404039708672"]]},{"metric":{"__name__":"node_memory_MemTotal_bytes","alias":"datacenteraggregation","cluster":"F10C1","datacenter":"us-mkc-ga-kvm-live","instance":"onode100103.server.lan:9100","job":"clusters"},"values":[[1698674400,"403904684032"],[1698674460,"403904684032"],[1698674520,"403904684032"],[1698674580,"403904684032"],[1698674640,"403904684032"],[1698674700,"403904684032"]]},{"metric":{"__name__":"node_memory_MemTotal_bytes","alias":"datacenteraggregation","cluster":"F10C1","datacenter":"us-mkc-ga-kvm-live","instance":"onode100104.server.lan:9100","job":"clusters"},"values":[[1698674400,"403904724992"],[1698674460,"403904724992"],[1698674520,"403904724992"],[1698674580,"403904724992"],[1698674640,"403904724992"],[1698674700,"403904724992"]]},{"metric":{"__name__":"node_memory_MemTotal_bytes","alias":"datacenteraggregation","cluster":"F10C1","datacenter":"us-mkc-ga-kvm-live","instance":"onode100105.server.lan:9100","job":"clusters"},"values":[[1698674400,"403904679936"],[1698674460,"403904679936"],[1698674520,"403904679936"],[1698674580,"403904679936"],[1698674640,"403904679936"],[1698674700,"403904679936"]]},{"metric":{"__name__":"node_memory_MemTotal_bytes","alias":"datacenter'
    handler = AvroSchemaHandler()
    schema = handler.create_schema(test_json)
    avro_schema = avro.schema.parse(json.dumps(schema))
    writer = DataFileWriter(BytesIO(), DatumWriter(), avro_schema)
    json_fix_handler = JsonFixHandler()
    complete_json = json_fix_handler.fix_json(test_json)
    writer.append(json.loads(complete_json))
    writer.close()
