// Copyright (c) 2024 Semjon Geist.

#ifndef CPPUTILS_STRING_OPERATIONS_HPP_
#define CPPUTILS_STRING_OPERATIONS_HPP_

#include <pybind11/eval.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <rapidjson/document.h>

#include <algorithm>
#include <chrono>
#include <datetime_utils.hpp>
#include <fstream>
#include <iostream>
#include <map>
#include <regex>
#include <sstream>
#include <utility>
#include <variant>
#include <vector>

using std::chrono::duration;
using std::chrono::duration_cast;
using std::chrono::high_resolution_clock;
using std::chrono::milliseconds;
namespace py = pybind11;

namespace string_operations {  // cppcheck-suppress syntaxError

inline const char *QUOTE_CHARS = "\"\'";
inline const char MINUS_CHAR = '-';
inline const char *HEX_CHAR = "0X";
inline const char TRUE_CHAR = 'T';
inline const char FALSE_CHAR = 'F';
inline const std::string SPECIAL_CHARS = "\r\n,;\t|\b";
inline const std::vector<std::string> NAN_STRINGS = {
    "NA", "NONE", "NULL", "UNDEFINED", "NONETYPE", "\"\""};
inline const std::regex hex_regex = std::regex("0[xX][0-9a-fA-F]+");
inline const std::regex boolean_true_regex =
    std::regex("true", std::regex::icase);
inline const std::regex boolean_false_regex =
    std::regex("false", std::regex::icase);
inline const std::regex numeric_regex =
    std::regex("(^([+-]?\\d[0-9]*)?(\\.(.*e-)?)?([0-9]*)?$)");
static const std::regex uuid_regex(
    "^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-["
    "089ab][0-9a-f]{3}-[0-9a-f]{12}$",
    std::regex_constants::icase);
static const std::regex ipv4_regex(
    R"(^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.){3}(25[0-5]|(2[0-4]|1\d|[1-9]|)\d)$)");

inline rapidjson::Document json_doc;
inline std::string ESCAPE_CHAR = "\\";
inline std::string PYTHON_ESCAPE_CHAR = "\\\\";
inline const char *JSON_CHARS = "{}";
inline const char *ARRAY_CHARS = "[]";

bool is_nan(std::string value);
bool is_quoted(const char &first_char, const char &last_char);
std::uint64_t parse64(std::string_view s) noexcept;
std::string replace_all(const std::string &data, const std::string &to_search,
                        const std::string &replace_str);
std::string trim(const std::string &str, const std::string &whitespace);
void preprocessJsonInPlace(std::string *input);
py::object to_generic_datetime(const std::string &value);
py::object eval_type(std::string value);
py::object eval_datetime(const std::string &value);
std::map<std::string, py::object> eval_csv(
    const std::string &input, const char *extra_disallowed_header_chars);
bool is_nan(std::string value);

std::string trim(const std::string &str, const std::string &whitespace = " \t");
//
// class JsonFlattenHandler : public
// rapidjson::BaseReaderHandler<rapidjson::UTF8<>, JsonFlattenHandler> {
// public:
//  JsonFlattenHandler();
//  struct JsonValue;
//
//  using JsonMap = std::map<std::string, JsonValue>;
//  using JsonArray = std::vector<JsonValue>;
//
//  struct JsonValue : std::variant<JsonMap, JsonArray, std::nullptr_t, bool,
//  int, unsigned, int64_t, uint64_t, double, std::string, py::object> {
//    using variant::variant; // Inherit constructors.
//  };
////  using JsonValue = std::variant<std::map<std::string, JsonValue>,
/// std::vector<JsonValue>, std::nullptr_t, bool, int, unsigned, int64_t,
/// uint64_t, double, std::string, py::object>;
//
//  bool StartObject();
//  bool EndObject(rapidjson::SizeType memberCount);
//  bool StartArray();
//  bool EndArray(rapidjson::SizeType elementCount);
//  bool Key(const char* str, rapidjson::SizeType length, bool copy);
//  bool String(const char* str, rapidjson::SizeType length, bool copy);
//  bool Int(int i);
//  bool Uint(unsigned u);
//  bool Bool(bool b);
//  bool Null();
//  bool Double(double d);
//  bool Int64(int64_t i);
//  bool Uint64(uint64_t u);
//
//  // Add declarations for other methods like Uint, Bool, Null, etc. if
//  necessary
//
//  bool parse_json_bytes(const std::string& json_bytes);
//  py::object create_flat_map() const;
//  py::object create_schema() const;
//
// private:
//  JsonArray schema;
//  JsonArray * objectsPtr;
//  std::vector<JsonArray *>  * nestedFieldsPtrStack;
//  std::vector<JsonArray *> objectsPtrStack;
//  std::map<JsonArray *, std::unordered_set<std::string>> fieldKeysStack;
//  std::map<std::string, JsonValue> flatMap;
//  std::vector<std::string> pathStack;
//  std::vector<int> indicesStack;
//  std::string currentKey;
//  std::string prefix;
////  bool isJsonStart;
////  bool jsonStartsWithArray;
//
////  void incrementIndexIfNeeded();
//  void set_value(JsonValue value, const std::string& type);
//  void add_record_or_array(const std::string& type);
//};
//
// struct JsonValueVisitor {
//  py::object operator()(const JsonFlattenHandler::JsonMap& map) const;
//  py::object operator()(const JsonFlattenHandler::JsonArray& array) const;
//  py::object operator()(std::nullptr_t) const;
//  py::object operator()(bool b) const;
//  py::object operator()(int i) const;
//  py::object operator()(unsigned u) const;
//  py::object operator()(int64_t i) const;
//  py::object operator()(uint64_t u) const;
//  py::object operator()(double d) const;
//  py::object operator()(const std::string& s) const;
//  py::object operator()(const py::object& obj) const;
//};
//
// py::object parse_json_value(const JsonFlattenHandler::JsonValue& value);

}  // namespace string_operations
#endif  // CPPUTILS_STRING_OPERATIONS_HPP_
