// Copyright (c) 2024 Semjon Geist.

//
// Created by sgeist on 09.02.24.
//
#include <string_operations.hpp>

namespace string_operations {

/// This is a simple C++ function to cast strings into python objects with
/// specific type
///
/// @param value string to cast
/// @returns python object (none, boolean, int, time, date, datetime,
/// datetime_ms, ip_address)
py::object eval_type(std::string value) {
  if (value.empty()) {
    return py::none();
  }

  int char_size = static_cast<int>(value.size());

  if (char_size <= 1) {
    if (std::isdigit(value.back())) return (py::cast(std::stoi(value)));
    return (py::cast(value));
  }

  // remove quote
  if (is_quoted(value[0], value.back())) {
    value = value.erase(0, 1).erase(char_size - 2);
    char_size = char_size - 2;

    if (value.empty()) {
      return py::none();
    }

    if (char_size == 1) {
      if (std::isdigit(value[0])) return (py::cast(std::stoi(&value[0])));
      return (py::cast(value[0]));
    }
  }

  // parse numeric
  if (std::regex_match(value, numeric_regex)) {
    if (value.find_first_of('.') != std::string::npos || value.back() == '.') {
      if (char_size > 18) {
        return (py::module::import("decimal").attr("Decimal")(value));
      }

      // parse double
      return (py::cast(std::stod(value)));
    }

    // parse numeric
    if (value[0] == MINUS_CHAR) {
      value = value.erase(0, 1);
      uint64_t integer = parse64(value);
      if (integer < UINT_MAX) {
        return (py::cast(-integer));
      }
      return (-py::module::import("builtins").attr("int")(value));
    }

    uint64_t integer = parse64(value);
    if (integer < UINT_MAX) {
      return (py::cast(integer));
    }
    return (py::module::import("builtins").attr("int")(value));
  }

  if (value.length() <= 2 && value[0] == ESCAPE_CHAR[0]) {
    if (value == "\\n") {
      return py::str("\n");
    } else if (value == "\\r") {
      return py::str("\r");
    } else if (value == "\\t") {
      return py::str("\t");
    } else if (value == "\\\\") {
      return py::str("\\");
    }
  }

  // is hex char
  if (value.length() <= 4 && value[0] == HEX_CHAR[0] &&
      std::toupper(value[1]) == HEX_CHAR[1] &&
      std::regex_match(value, hex_regex)) {
    return py::cast(std::stoul(value, nullptr, 16));
  }

  const char upper_first_char = static_cast<char>(std::toupper(value[0]));

  // boolean true or boolan false
  if (char_size < 6 &&
      (upper_first_char == TRUE_CHAR || upper_first_char == FALSE_CHAR)) {
    if (std::regex_match(value, boolean_true_regex)) {
      return (py::cast(true));
    }

    if (std::regex_match(value, boolean_false_regex)) {
      return (py::cast(false));
    }
  }

  if (is_nan(value)) {
    return (py::cast<py::none>(Py_None));
  }

  if (char_size == 36 && std::regex_match(value, uuid_regex)) {
    return (py::module::import("uuid").attr("UUID")(value));
  }

  const char last_char = value.back();

  if ((value[0] == JSON_CHARS[0] && last_char == JSON_CHARS[1]) ||
      (value[0] == ARRAY_CHARS[0] && last_char == ARRAY_CHARS[1])) {
    std::string json_value =
        replace_all(value, ESCAPE_CHAR, PYTHON_ESCAPE_CHAR);
    preprocessJsonInPlace(&json_value);
    if (!json_doc.Parse(const_cast<char *>(json_value.c_str()))
             .HasParseError()) {
      return py::eval(json_value);
    }
  }

  if (char_size < 6) {
    // normal string
    return py::cast(value);
  }

  // ipv4
  if (char_size < 39 && char_size > 6) {
    // ipv4
    if (std::count(value.begin(), value.end(), '.') == 3 &&
        std::regex_match(value, ipv4_regex)) {
      return (py::module::import("ipaddress").attr("IPv4Address")(value));
    }
    // ipv6
    if (std::count(value.begin(), value.end(), ':') > 5) {
      try {
        return (py::module::import("ipaddress").attr("IPv6Address")(value));
      } catch (...) {
      }
    }
    if (char_size > 7) {
      return (to_generic_datetime(value));
    }
  }

  // normal string
  return py::cast(value);
}
}  // namespace string_operations
