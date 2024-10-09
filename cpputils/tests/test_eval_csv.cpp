// Copyright (c) 2024 Semjon Geist.

//
// Created by sgeist on 12.02.24.
//
#include <pybind11/pybind11.h>

#include <iostream>
#include <tests/catch2.hpp>

// pybind11 code not working with Catch2 (need to separate cpp from pybdin11
// code)

// TEST_CASE("eval_csv correctly parses cdv and generates schema",
//           "[JsonHandler]") {
//   // Example JSON string that includes various types
//   std::string csv_bytes =
//       R"(ID,Name,Age,Email,Salary,FullTime,JoinDate,Rating,Address,Skills
// 1,Alice,28,alice@example.com,50000.0,True,2022-01-01,4.5,"{\'Street\': \'123
// Maple Street\', \'City\': \'Springfield\', \'Zip\': \'12345\'}","[\'Python\',
// \'SQL\', \'Java\']"
// 2,Bob,34,bob@example.com,60000.0,False,2022-06-15,3.8,"{\'Street\': \'456 Oak
// Street\', \'City\': \'Shelbyville\', \'Zip\': \'67890\'}","[\'Java\', \'C#\',
// \'JavaScript\']"
// 3,Charlie,23,charlie@example.com,55000.0,True,2023-02-20,4.2,"{\'Street\':
// \'789 Pine Street\', \'City\': \'Capital City\', \'Zip\':
// \'54321\'}","[\'HTML\', \'CSS\', \'JavaScript\']"
//)";
//   std::map<std::string, py::object> csv_schema =
//   string_operations::eval_csv(csv_bytes, ""); REQUIRE(!csv_schema.empty());
// }
