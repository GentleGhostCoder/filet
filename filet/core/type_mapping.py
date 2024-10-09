from enum import Enum, EnumMeta


class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class TrinoPythonTypesMapping(Enum, metaclass=MetaEnum):
    """Representation of Python to Trino specific data type classes."""

    NULL = "NoneType"
    VARCHAR = "str"
    TIMESTAMP = "datetime"
    TIME = "time"
    INTEGER = "int"
    DOUBLE = "float"
    DECIMAL = "Decimal"
    IPADDRESS = "IPv4Address"
    BOOLEAN = "bool"
    UUID = "UUID"
    VARBINARY = "bytes"
    nan = "nan"
    IPv6Address = "IPv6Address"
    ARRAY = "list"
    JSON = "dict"
    DATE = "date"


class TrinoAvroTypeMapping(Enum, metaclass=MetaEnum):
    """Representation of Avro to Trino specific data type classes."""

    NULL = "null"
    BOOLEAN = "boolean"
    VARCHAR = "string"
    BIGINT = "int"
    DOUBLE = "double"
    DECIMAL = "decimal"


class JsonType(Enum, metaclass=MetaEnum):
    """
    Represents the JSON types used in Avro schema.
    """

    array = "array"
    record = "record"
    unknown = "unknown"
    string = "string"
    int = "int"
    double = "double"
    null = "null"
    boolean = "boolean"
    union = "union"


class JsonFormat(Enum, metaclass=MetaEnum):
    txt = "txt"
    flat = "flat"
    avro = "avro"
    # TODO: Add json lines maybe as well
