// Copyright (c) 2024 Semjon Geist.

// Copyright (c) 2022 Semjon Geist.

#ifndef CPPUTILS_EVAL_JSON_HPP_
#define CPPUTILS_EVAL_JSON_HPP_

#include <rapidjson/error/en.h>

#include <iostream>
#include <logging.hpp>
#include <set>
#include <stdexcept>
#include <string>
#include <string_operations.hpp>
#include <unordered_set>
namespace py = pybind11;

namespace json {  // cppcheck-suppress syntaxError

struct JsonValue;

using JsonMap = std::unordered_map<std::string, JsonValue>;
using JsonArray = std::vector<JsonValue>;

struct JsonValue
    : std::variant<JsonMap, JsonArray, std::nullptr_t, bool, int, unsigned,
                   int64_t, uint64_t, double, std::string, py::object> {
  using variant::variant;  // Inherit constructors.
};

enum class JsonType { Array, Record, Unknown };

struct SchemaElement {
  JsonType type = JsonType::Unknown;
  JsonArray* objectsPtr = nullptr;
  std::string prefix;
  std::string key;
  std::int64_t index;

  // Constructor for when objectsPtr is provided.
  SchemaElement(JsonType type, JsonArray* objectsPtr, std::string currentPrefix,
                std::string currentKey, int index)
      : type(type),
        objectsPtr(objectsPtr),
        prefix(std::move(currentPrefix)),
        key(std::move(currentKey)),
        index(index) {}

  // Overloaded constructor for when objectsPtr is not provided.
  SchemaElement(JsonType type, std::string currentPrefix,
                std::string currentKey, int index)
      : type(type),
        prefix(std::move(currentPrefix)),
        key(std::move(currentKey)),
        index(index) {}

  // Overloaded constructor for when objectsPtr and type is not provided.
  SchemaElement(std::string currentPrefix, std::string currentKey, int index)
      : prefix(std::move(currentPrefix)),
        key(std::move(currentKey)),
        index(index) {}

  // Delete copy constructor and copy assignment operator to prevent copying.
  SchemaElement(const SchemaElement&) = delete;
  SchemaElement& operator=(const SchemaElement&) = delete;

  // Move constructor.
  SchemaElement(SchemaElement&& other) noexcept
      : type(other.type),
        objectsPtr(other.objectsPtr),
        prefix(std::move(other.prefix)),
        key(std::move(other.key)),
        index(other.index) {
    // Optional: explicitly set other.objectsPtr to nullopt if needed.
  }

  // Move assignment operator.
  SchemaElement& operator=(SchemaElement&& other) noexcept {
    if (this != &other) {
      type = other.type;
      objectsPtr = other.objectsPtr;
      prefix = std::move(other.prefix);
      key = std::move(other.key);
      index = other.index;
      // Optional: explicitly set other.objectsPtr to nullopt if needed.
    }
    return *this;
  }
};

class JsonHandler
    : public rapidjson::BaseReaderHandler<rapidjson::UTF8<>, JsonHandler> {
 public:
  virtual bool StartObject() { return true; }
  virtual bool EndObject(rapidjson::SizeType) { return true; }
  virtual bool StartArray() { return true; }
  virtual bool EndArray(rapidjson::SizeType) { return true; }
  virtual bool Key(const char* str, rapidjson::SizeType length, bool copy) {
    return true;
  }
  virtual bool String(const char* str, rapidjson::SizeType length, bool copy) {
    return true;
  }
  virtual bool Int(int i) { return true; }
  virtual bool Uint(unsigned u) { return true; }
  virtual bool Bool(bool b) { return true; }
  virtual bool Null() { return true; }
  virtual bool Double(double d) { return true; }
  virtual bool Int64(int64_t i) { return true; }
  virtual bool Uint64(uint64_t u) { return true; }
  virtual bool RawNumber(const char* str, rapidjson::SizeType length,
                         bool copy) {
    return true;
  }

  bool parse_json_bytes(const std::string& json_bytes);

 private:
  rapidjson::Reader reader;
  std::string buffer;
};

class AvroSchemaHandler : public JsonHandler {
 public:
  using JsonHandler::JsonHandler;  // Inherit constructors
  AvroSchemaHandler();
  bool StartObject() override;
  bool EndObject(rapidjson::SizeType memberCount) override;
  bool StartArray() override;
  bool EndArray(rapidjson::SizeType elementCount) override;
  bool Key(const char* str, rapidjson::SizeType length, bool copy) override;
  bool String(const char* str, rapidjson::SizeType length, bool copy) override;
  bool Int(int i) override;
  bool Uint(unsigned u) override;
  bool Bool(bool b) override;
  bool Null() override;
  bool Double(double d) override;
  bool Int64(int64_t i) override;
  bool Uint64(uint64_t u) override;
  bool RawNumber(const char* str, rapidjson::SizeType length,
                 bool copy) override;
  py::object create_schema(const std::string& json_bytes);
  bool read_existing_schema(const py::dict& existingSchema);
  py::object update_schema(const py::dict& schema);
  py::object get_schema();

 private:
  JsonArray schema;
  std::vector<SchemaElement> schema_ptr_stack;
  bool schema_exists;
  void set_type(const std::string& type);
  void recursive_update(JsonValue* d, const JsonValue& u);
  void create_union_types(JsonArray* items);
  static std::pair<std::string, std::string> get_type(const JsonValue& item);
  static bool exists_in_array(const JsonArray& array, const JsonValue& item);
  static JsonArray validate_schema(const py::dict& schema);
  void reset_schema();
  static void set_compatibility(JsonArray* items1, JsonArray* items2);
};

class FlatJsonHandler : public JsonHandler {
 public:
  using JsonHandler::JsonHandler;  // Inherit constructors
  FlatJsonHandler();
  bool StartObject() override;
  bool EndObject(rapidjson::SizeType memberCount) override;
  bool StartArray() override;
  bool EndArray(rapidjson::SizeType elementCount) override;
  bool Key(const char* str, rapidjson::SizeType length, bool copy) override;
  bool String(const char* str, rapidjson::SizeType length, bool copy) override;
  bool Int(int i) override;
  bool Uint(unsigned u) override;
  bool Bool(bool b) override;
  bool Null() override;
  bool Double(double d) override;
  bool Int64(int64_t i) override;
  bool Uint64(uint64_t u) override;
  bool RawNumber(const char* str, rapidjson::SizeType length,
                 bool copy) override;
  py::object loads(const std::string& data);
  py::object header();

 private:
  JsonMap current_row;
  JsonMap output_rows;
  std::uint64_t row_idx;
  std::string buffer;
  bool starts_with_array{};
  std::int64_t row_depth;
  std::vector<SchemaElement> schema_ptr_stack;
  void clear_row(const std::string& prefix);
  void insert_rows(JsonType type, std::int64_t current_depth,
                   const std::string& prefix);
  void set_type(const JsonValue& value);
  std::string create_prefix(const std::string& prefix, const std::string& key);
};

struct JsonValueVisitor {
  py::object operator()(const JsonMap& map) const;
  py::object operator()(const JsonArray& array) const;
  py::object operator()(std::nullptr_t) const;
  py::object operator()(bool b) const;
  py::object operator()(int i) const;
  py::object operator()(unsigned u) const;
  py::object operator()(int64_t i) const;
  py::object operator()(uint64_t u) const;
  py::object operator()(double d) const;
  py::object operator()(const std::string& s) const;
  py::object operator()(const py::object& obj) const;
};

py::object parse_json_value(const JsonValue& value);

class PythonDictVisitor {
 public:
  JsonValue operator()(const py::object& obj) const;

 private:
  JsonValue visit_dict(const py::dict& dict) const;
  JsonValue visit_list(const py::list& list) const;
  static JsonValue visit_none();
  static JsonValue visit_bool(const py::bool_& b);
  static JsonValue visit_int(const py::int_& i);
  static JsonValue visit_float(const py::float_& f);
  static JsonValue visit_str(const py::str& s);
};

JsonValue parse_python_dict(const py::dict& obj);

class PyJsonFlattenHandler : public JsonHandler {
 public:
  using JsonHandler::JsonHandler;  // Inherit constructors

  bool StartObject() override {
    PYBIND11_OVERRIDE(bool, JsonHandler, StartObject);
  }
  bool EndObject(rapidjson::SizeType memberCount) override {
    PYBIND11_OVERRIDE(bool, JsonHandler, EndObject, memberCount);
  }
  bool StartArray() override {
    PYBIND11_OVERRIDE(bool, JsonHandler, StartArray);
  }
  bool EndArray(rapidjson::SizeType elementCount) override {
    PYBIND11_OVERRIDE(bool, JsonHandler, EndArray, elementCount);
  }
  bool Key(const char* str, rapidjson::SizeType length, bool copy) override {
    PYBIND11_OVERRIDE(bool, JsonHandler, Key, str, length, copy);
  }
  bool String(const char* str, rapidjson::SizeType length, bool copy) override {
    PYBIND11_OVERRIDE(bool, JsonHandler, String, str, length, copy);
  }
  bool Int(int i) override { PYBIND11_OVERRIDE(bool, JsonHandler, Int, i); }
  bool Uint(unsigned u) override {
    PYBIND11_OVERRIDE(bool, JsonHandler, Uint, u);
  }
  bool Bool(bool b) override { PYBIND11_OVERRIDE(bool, JsonHandler, Bool, b); }
  bool Null() override { PYBIND11_OVERRIDE(bool, JsonHandler, Null); }
  bool Double(double d) override {
    PYBIND11_OVERRIDE(bool, JsonHandler, Double, d);
  }
  bool Int64(int64_t i) override {
    PYBIND11_OVERRIDE(bool, JsonHandler, Int64, i);
  }
  bool Uint64(uint64_t u) override {
    PYBIND11_OVERRIDE(bool, JsonHandler, Uint64, u);
  }
  bool RawNumber(const char* str, rapidjson::SizeType length,
                 bool copy) override {
    PYBIND11_OVERRIDE(bool, JsonHandler, RawNumber, str, length, copy);
  }
};

}  // namespace json
#endif  // CPPUTILS_EVAL_JSON_HPP_
