// Copyright (c) 2024 Semjon Geist.

//
// Created by sgeist on 12.02.24.
//
#include <tests/catch2.hpp>

// pybind11 code not working with Catch2 (need to separate cpp from pybind11
// code)
//
// TEST_CASE("parse_json_bytes correctly parses JSON and generates Avro schema",
//          "[JsonHandler]") {
//  json::AvroSchemaHandler handler;
//  // Example JSON string that includes various types
//  std::string json_bytes = R"({
//      "id": "001",
//      "name": "Complex Data Object",
//      "isActive": true,
//      "counts": [1, null, 3],
//      "tags": ["data", "test", null],
//      "metadata": {
//        "createdDate": "2024-02-08",
//        "updatedDate": null,
//        "contributors": [
//          {
//            "name": "John Doe",
//            "roles": ["author"],
//            "contact": {
//              "email": "john.doe@example.com",
//              "phoneNumbers": ["123-456-7890", null]
//            }
//          },
//          {
//            "name": "Jane Smith",
//            "roles": ["editor", "contributor"],
//            "contact": {
//              "email": "jane.smith@example.com",
//              "phoneNumbers": []
//            }
//          }
//        ]
//      },
//      "relatedObjects": [
//        {
//          "id": "002",
//          "type": "relatedType",
//          "properties": {
//            "property1": "value1",
//            "property2": 2,
//            "property3": true,
//            "property4": null
//          }
//        }
//      ],
//      "optionalField": null,
//      "miscellaneous": {
//        "anyOf": [
//          {
//            "type": "type1",
//            "description": "A type1 object",
//            "details": {
//              "detail1": "Some detail"
//            }
//          },
//          "simpleString",
//          42,
//          true
//        ]
//      },
//      "numericData": {
//        "integerValue": 123,
//        "floatValue": 123.456,
//        "doubleValue": null
//      },
//      "booleanFlags": {
//        "flag1": true,
//        "flag2": false,
//        "flag3": null
//      },
//      "emptyArray": [],
//      "complexArray": [
//        ["nested", "array"],
//        [],
//        [1, 2, 3],
//        [null, {"key": "value"}, true]
//      ],
//      "unionType": [
//        "stringValue",
//        789,
//        true,
//        null,
//        {
//          "unionObject": "data"
//        }
//      ]
//    })";
//  REQUIRE(handler.parse_json_bytes(json_bytes) == true);
//}
