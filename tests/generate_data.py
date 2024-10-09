"""Units methods to generate test data."""

import copy
import json

import pandas as pd


# Function to generate simple data
def generate_simple_csv_data():
    data = {
        "ID": [1, 2, 3],
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [28, 34, 23],
        "Email": ["alice@example.com", "bob@example.com", "charlie@example.com"],
        "Salary": [50000.00, 60000.00, 55000.00],
        "FullTime": [True, False, True],
        "JoinDate": ["2022-01-01", "2022-06-15", "2023-02-20"],
        "Rating": [4.5, 3.8, 4.2],
    }
    df = pd.DataFrame(data)
    return df


# Function to generate complex data
def generate_complex_csv_data():
    data = {
        "ID": [1, 2, 3],
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [28, 34, 23],
        "Email": ["alice@example.com", "bob@example.com", "charlie@example.com"],
        "Salary": [50000.00, 60000.00, 55000.00],
        "FullTime": [True, False, True],
        "JoinDate": ["2022-01-01", "2022-06-15", "2023-02-20"],
        "Rating": [4.5, 3.8, 4.2],
        "Address": [
            {"Street": "123 Maple Street", "City": "Springfield", "Zip": "12345"},
            {"Street": "456 Oak Street", "City": "Shelbyville", "Zip": "67890"},
            {"Street": "789 Pine Street", "City": "Capital City", "Zip": "54321"},
        ],
        "Skills": [["Python", "SQL", "Java"], ["Java", "C#", "JavaScript"], ["HTML", "CSS", "JavaScript"]],
    }
    df = pd.DataFrame(data)
    return df


def _enrich_arrays(obj, enrichment_count=1, enrichment_strategy="duplicate_last"):
    """Enrich the arrays in a JSON object by duplicating the last item or adding a custom item."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (list, dict)):
                obj[key] = _enrich_arrays(value, enrichment_count, enrichment_strategy)
    elif isinstance(obj, list):
        # Check the enrichment strategy
        if enrichment_strategy == "duplicate_last":
            # Duplicate the last item or add a placeholder if the array is empty
            for _ in range(enrichment_count):
                if obj:
                    new_item = copy.deepcopy(obj[-1])  # Deep copy to handle nested structures
                    obj.append(new_item)
                else:
                    obj.append("enriched_empty")
        elif enrichment_strategy == "add_custom":
            # Add a custom item, could be based on the index or any other logic
            for i in range(enrichment_count):
                obj.append(f"custom_enriched_item_{i}")
        # Apply the enrichment recursively for items within the array
        for i, item in enumerate(obj):
            obj[i] = _enrich_arrays(item, enrichment_count, enrichment_strategy)
    return obj


def generate_complex_json_data():
    # Original JSON data
    data = """
    {
      "id": "001",
      "name": "Complex Data Object",
      "isActive": true,
      "counts": [1, null, 3],
      "tags": ["data", "test", null],
      "metadata": {
        "createdDate": "2024-02-08",
        "updatedDate": null,
        "contributors": [
          {
            "name": "John Doe",
            "roles": ["author"],
            "contact": {
              "email": "john.doe@example.com",
              "phoneNumbers": ["123-456-7890", null]
            }
          },
          {
            "name": "Jane Smith",
            "roles": ["editor", "contributor"],
            "contact": {
              "email": "jane.smith@example.com",
              "phoneNumbers": []
            }
          }
        ]
      },
      "relatedObjects": [
        {
          "id": "002",
          "type": "relatedType",
          "properties": {
            "property1": "value1",
            "property2": 2,
            "property3": true,
            "property4": null
          }
        }
      ],
      "optionalField": null,
      "numericData": {
        "integerValue": 123,
        "floatValue": 123.456,
        "doubleValue": null
      },
      "booleanFlags": {
        "flag1": true,
        "flag2": false,
        "flag3": null
      },
      "emptyArray": [],
      "anotherRecord": {
          "test": [1, 2, 3],
          "user": {
            "name": "John Doe",
            "age": 30,
            "emails": [
              "john.doe@example.com",
              "johnny@example.com"
            ],
            "address": {
              "street": "123 Main St",
              "city": "Anytown",
              "zipCode": "12345"
            }
          },
          "products": [
                {
                  "id": 1,
                  "name": "Product 1",
                  "tags": ["Tag1", null, "Tag2"]
                },
                {
                  "id": 2,
                  "name": "Product 2",
                  "tags": ["Tag1", null, "Tag2"],
                  "flags": {
                    "flag1": true,
                    "flag2": false
                  }
                }
            ]
        },
         "prometheus": {
            "status": "success",
            "data": {
                "resultType": "matrix",
                "result": [
                    {
                        "metric": {
                            "__name__": "node_memory_MemTotal_bytes",
                            "test": "test",
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
                    },
                    {"metric":{"__name__":"node_cpu_seconds_total","cpu":"0","instance":"osum-ekca-live-bap01.pki.server.lan:9100","job":"pki","mode":"iowait","type":"pki"},"values":[[1698674400,"654.78"],[1698674460,"654.78"],[1698674520,"654.78"],[1698674580,"654.78"],[1698674640,"654.83"],[1698674700,"654.83"]]}
                ]
            }
        }
    }
    """

    # currently not working for trino:
    # TODO: evaluate
    # "complexArray": [
    #     ["nested", "array"],
    #     [],
    #     [[1, 2, 3]],
    #     [1, 2, 3],
    #     [null, {"key": "value"}, true]
    # ],
    #
    #
    # "unionType": [
    #     "stringValue",
    #     789,
    #     true,
    #     null,
    #     {
    #         "unionObject": "data"
    #     }
    # ],
    # "miscellaneous": {
    #     "anyOf": [
    #         {
    #             "type": "type1",
    #             "description": "A type1 object",
    #             "details": {
    #                 "detail1": "Some detail"
    #             }
    #         },
    #         "simpleString",
    #         42,
    #         true
    #     ]
    # },
    enriched_data = json.dumps(_enrich_arrays(json.loads(data), 10, "duplicate_last"))
    # print(json.dumps(enriched_data, indent=2))
    return enriched_data


def generate_complex_union_json_data():
    data = """
    {
      "id": "001",
      "name": "Complex Data Object",
      "isActive": true,
      "counts": [1, null, 3],
      "tags": ["data", "test", null],
      "metadata": {
        "createdDate": "2024-02-08",
        "updatedDate": null,
        "contributors": [
          {
            "name": "John Doe",
            "roles": ["author"],
            "contact": {
              "email": "john.doe@example.com",
              "phoneNumbers": ["123-456-7890", null]
            }
          },
          {
            "name": "Jane Smith",
            "roles": ["editor", "contributor"],
            "contact": {
              "email": "jane.smith@example.com",
              "phoneNumbers": []
            }
          }
        ]
      },
      "relatedObjects": [
        {
          "id": "002",
          "type": "relatedType",
          "properties": {
            "property1": "value1",
            "property2": 2,
            "property3": true,
            "property4": null
          }
        }
      ],
      "optionalField": null,
      "miscellaneous": {
        "anyOf": [
          {
            "type": "type1",
            "description": "A type1 object",
            "details": {
              "detail1": "Some detail"
            }
          },
          "simpleString",
          42,
          true
        ]
      },
      "numericData": {
        "integerValue": 123,
        "floatValue": 123.456,
        "doubleValue": null
      },
      "booleanFlags": {
        "flag1": true,
        "flag2": false,
        "flag3": null
      },
      "emptyArray": [],
      "complexArray": [
        ["nested", "array"],
        [],
        [[1, 2, 3]],
        [1, 2, 3],
        [null, {"key": "value"}, true]
      ],
      "unionType": [
        "stringValue",
        789,
        true,
        null,
        {
          "unionObject": "data"
        }
      ],
      "anotherRecord": {
          "test": [1, 2, 3],
          "user": {
            "name": "John Doe",
            "age": 30,
            "emails": [
              "john.doe@example.com",
              "johnny@example.com"
            ],
            "address": {
              "street": "123 Main St",
              "city": "Anytown",
              "zipCode": "12345"
            }
          },
          "products": [
                {
                  "id": 1,
                  "name": "Product 1",
                  "tags": ["Tag1", null, "Tag2"]
                },
                {
                  "id": 2,
                  "name": "Product 2",
                  "tags": ["Tag1", null, "Tag2"],
                  "flags": {
                    "flag1": true,
                    "flag2": false
                  }
                }
            ]
        },
         "prometheus": {
            "status": "success",
            "data": {
                "resultType": "matrix",
                "result": [
                    {
                        "metric": {
                            "__name__": "node_memory_MemTotal_bytes",
                            "test": "test",
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
                    },
                    {"metric":{"__name__":"node_cpu_seconds_total","cpu":"0","instance":"osum-ekca-live-bap01.pki.server.lan:9100","job":"pki","mode":"iowait","type":"pki"},"values":[[1698674400,"654.78"],[1698674460,"654.78"],[1698674520,"654.78"],[1698674580,"654.78"],[1698674640,"654.83"],[1698674700,"654.83"]]}
                ]
            }
        }
    }"""
    enriched_data = json.dumps(_enrich_arrays(json.loads(data), 10, "duplicate_last"))
    # print(json.dumps(enriched_data, indent=2))
    return enriched_data


def generate_simple_json_data():
    # Original JSON data
    data = """
    {
      "header": {
        "documentTitle": "Sample Document",
        "creationDate": "2024-02-12",
        "author": "John Doe",
        "version": 1.0
      },
      "data": [
        [
          {"id": 1, "name": "Item One", "quantity": 3, "price": 19.99},
          {"id": 2, "name": "Item Two", "quantity": 5, "price": 7.99}
        ],
        [
          {"id": 3, "name": "Item Three", "quantity": 2, "price": 15.49},
          {"id": 4, "name": "Item Four", "quantity": 4, "price": 5.99}
        ]
      ]
    }
    """

    enriched_data = json.dumps(_enrich_arrays(json.loads(data), 10, "duplicate_last"))
    # print(json.dumps(enriched_data, indent=2))
    return enriched_data
