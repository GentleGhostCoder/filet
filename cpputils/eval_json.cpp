// Copyright (c) 2024 Semjon Geist.

//
// Created by sgeist on 09.02.24.
//
#include <eval_json.hpp>
#include <utility>

namespace json {

bool JsonHandler::parse_json_bytes(const std::string &json_bytes) {
  //  buffer += json_bytes; // Append new chunk to buffer
  rapidjson::StringStream ss(json_bytes.c_str());

  // Reset the reader before each parse attempt to clear any previous state
  rapidjson::ParseResult result = reader.Parse(ss, *this);

  if (result) {
    return true;
  }
  return false;
}

FlatJsonHandler::FlatJsonHandler()
    : schema_ptr_stack(), row_idx(0), row_depth(0), starts_with_array(false) {
  schema_ptr_stack.emplace_back("", "root", 0);
}

py::object FlatJsonHandler::loads(const std::string &data) {
  // check if data starts with an array
  starts_with_array = data[0] == '[';
  output_rows.clear();
  row_idx = 0;
  parse_json_bytes(data);
  return (parse_json_value(output_rows));
}

py::object FlatJsonHandler::header() {
  return parse_json_value(output_rows).attr("keys")();
}

std::string FlatJsonHandler::create_prefix(const std::string &prefix,
                                           const std::string &key) {
  if (prefix.empty()) return key;
  return prefix + '_' + key;
}

void FlatJsonHandler::set_type(const JsonValue &value) {
  auto &[current_type, _, current_prefix, current_key, index] =
      schema_ptr_stack.back();
  std::string new_key = current_key;
  bool is_simple_union = false;
  if (current_key.empty() && current_prefix.back() == '_') {
    is_simple_union = true;
    new_key = std::to_string(index);
    index++;
  }
  new_key = create_prefix(current_prefix, new_key);
  // get index of current key in map keys of output_rows
  bool header_exists = current_row.find(new_key) != current_row.end();

  // if key is not in header_names, add it
  if (!header_exists) {
    current_row.insert({new_key, value});
    if (!is_simple_union && current_type == JsonType::Array) {
      insert_rows(current_type, schema_ptr_stack.size() - 1, new_key);
    }
    return;
  }
  current_row[new_key] = value;
  if (!is_simple_union && current_type == JsonType::Array) {
    insert_rows(current_type, schema_ptr_stack.size() - 1, new_key);
  }
}

bool FlatJsonHandler::StartArray() {
  auto &[current_type, _, current_prefix, current_key, index] =
      schema_ptr_stack.back();
  index += 1;
  if (current_key.empty() && row_depth == 0) {
    // init row_depth
    row_depth = schema_ptr_stack.size() + 1;
  }
  if (!starts_with_array && row_depth != 0) {
    clear_row(schema_ptr_stack[row_depth].prefix);
  }
  std::string new_key = create_prefix(current_prefix, current_key);
  schema_ptr_stack.emplace_back(JsonType::Array, new_key, "", 0);
  return true;
}

bool FlatJsonHandler::StartObject() {
  auto &[current_type, _, current_prefix, current_key, index] =
      schema_ptr_stack.back();
  index++;
  if (current_key.empty() && row_depth == 0) {
    // init row_depth
    row_depth = schema_ptr_stack.size() + 1;
  }
  if (!starts_with_array && row_depth != 0) {
    clear_row(schema_ptr_stack[row_depth - 1].prefix);
  }
  std::string new_key = create_prefix(current_prefix, current_key);
  schema_ptr_stack.emplace_back(JsonType::Record, new_key, "", 0);
  return true;
}

void FlatJsonHandler::insert_rows(JsonType type, std::int64_t current_depth,
                                  const std::string &prefix) {
  if (current_depth <= row_depth) {
    clear_row(prefix);
    return;
  }
  // Avoid processing if not necessary
  if (!(starts_with_array || type == JsonType::Array)) return;

  // Assume resizing less frequently can improve performance
  size_t new_size = row_idx + 1;
  for (auto &[key, value] : current_row) {
    // Directly work with substring view to avoid copying when not necessary
    std::string_view col_key_view(key);
    col_key_view.remove_prefix(5);  // Adjust according to your logic
    std::string col_key(
        col_key_view);  // Convert to string if necessary for map operations

    // Use emplace to avoid double lookup
    auto [iter, inserted] = output_rows.emplace(col_key, JsonArray{});
    if (inserted) {
      iter->second =
          JsonArray(new_size);  // Directly allocate with the new size
    } else {
      auto &array = std::get<JsonArray>(iter->second);
      if (array.size() < new_size) {
        array.resize(new_size);  // Resize only if needed
      }
    }
    std::get<JsonArray>(iter->second)[row_idx] = value;
  }
  row_idx++;
  clear_row(prefix);
}

void FlatJsonHandler::clear_row(const std::string &prefix) {
  //   Remove all keys from the current row that have the same prefix in their
  //   name (starts with)
  for (auto &[key, value] : current_row) {
    if (key.rfind(prefix, 0) ==
        0) {  // If the key starts with the parent_prefix
      value = py::none();
    }
  }
}

bool FlatJsonHandler::EndObject(rapidjson::SizeType) {
  auto &[current_type, _, parent_prefix, parent_key, index] =
      schema_ptr_stack.back();
  if (starts_with_array && parent_prefix == "root_") {
    insert_rows(current_type, row_depth + 1, parent_prefix);
  }
  if (current_type != JsonType::Array) {
    schema_ptr_stack.pop_back();
    return true;
  }
  insert_rows(current_type, schema_ptr_stack.size(), parent_prefix);
  schema_ptr_stack.pop_back();
  return true;
}

bool FlatJsonHandler::EndArray(rapidjson::SizeType) {
  auto &[current_type, _, current_prefix, current_key, index] =
      schema_ptr_stack.back();
  if (index > 1) {
    // is union type
    insert_rows(current_type, schema_ptr_stack.size() - 1, current_prefix);
  }
  schema_ptr_stack.pop_back();  // reduce depth
  return true;
}

bool FlatJsonHandler::Key(const char *str, rapidjson::SizeType length,
                          bool copy) {
  schema_ptr_stack.back().key = std::string(str, length);
  return true;
}

bool FlatJsonHandler::String(const char *str, rapidjson::SizeType length,
                             bool copy) {
  set_type(std::string(str, length));
  return true;
}

bool FlatJsonHandler::Int(int i) {
  set_type(i);
  return true;
}

bool FlatJsonHandler::Uint(unsigned u) {
  set_type(u);
  return true;
}

bool FlatJsonHandler::Double(double d) {
  set_type(d);
  return true;
}

bool FlatJsonHandler::Int64(int64_t i) {
  set_type(i);
  return true;
}

bool FlatJsonHandler::Uint64(uint64_t u) {
  set_type(u);
  return true;
}

bool FlatJsonHandler::Null() {
  set_type(nullptr);
  return true;
}

bool FlatJsonHandler::Bool(bool b) {
  set_type(b);
  return true;
}

bool FlatJsonHandler::RawNumber(const char *str, rapidjson::SizeType length,
                                bool copy) {
  set_type(std::string(str, length));
  return true;
}

AvroSchemaHandler::AvroSchemaHandler()
    : schema(JsonArray()), schema_ptr_stack(), schema_exists(false) {
  schema_ptr_stack.emplace_back(JsonType::Array, &schema, "", "root", 0);
}

bool AvroSchemaHandler::read_existing_schema(const py::dict &existingSchema) {
  // Assuming here that the existing schema is in the correct format and can be
  // directly used as input.
  reset_schema();
  schema = validate_schema(existingSchema);
  if (schema.empty()) {
    return false;
  }
  schema_exists = true;
  return true;
}

void AvroSchemaHandler::reset_schema() {
  schema = JsonArray();
  while (!schema_ptr_stack.empty()) {
    schema_ptr_stack.pop_back();
  }
  schema_ptr_stack.emplace_back(JsonType::Array, &schema, "", "root", 0);
  schema_exists = false;
}

JsonArray AvroSchemaHandler::validate_schema(const py::dict &schema) {
  // TODO(sgeist): implement more validation checks
  JsonValue _schema = parse_python_dict(schema);
  if (std::variant(_schema).valueless_by_exception()) {
    return {};
  }
  if (std::holds_alternative<JsonArray>(_schema)) {
    return std::get<JsonArray>(_schema);
  } else if (std::holds_alternative<JsonMap>(_schema)) {
    return JsonArray{
        JsonMap{{"name", "root"}, {"type", std::get<JsonMap>(_schema)}}};
  } else {
    return {};
  }
}

py::object AvroSchemaHandler::update_schema(const py::dict &new_schema) {
  if (!schema_exists) {
    read_existing_schema(new_schema);
    return get_schema();
  }
  JsonArray new_schema_array = validate_schema(new_schema);
  recursive_update(&schema[0], new_schema_array[0]);
  return get_schema();
}

py::object AvroSchemaHandler::get_schema() {
  return parse_json_value(
      std::get<JsonMap>(std::get<JsonMap>(schema[0])["type"]));
}

py::object AvroSchemaHandler::create_schema(const std::string &json_bytes) {
  if (schema_exists) {
    // copy old `schema` into old_schema
    JsonArray old_schema = schema;
    reset_schema();
    parse_json_bytes(json_bytes);
    schema_exists = true;
    recursive_update(&old_schema[0], schema[0]);
    schema = old_schema;  // replace with updated schema
    return get_schema();
  }
  parse_json_bytes(json_bytes);
  schema_exists = true;
  return get_schema();
}

void AvroSchemaHandler::set_type(const std::string &type) {
  auto &[current_type, current_schema_ptr, current_prefix, current_key, index] =
      schema_ptr_stack.back();

  // Check if we are dealing with a named field within an object/schema.
  if (!current_key.empty()) {
    auto &back = schema_ptr_stack.back();
    auto existing_field_iter = find_if(
        current_schema_ptr->begin(), current_schema_ptr->end(),
        [&back](const JsonValue &obj) {  // Capture current_key correctly
          return std::holds_alternative<JsonMap>(obj) &&
                 std::get<std::string>(std::get<JsonMap>(obj).at("name")) ==
                     back.key;
        });

    if (existing_field_iter != current_schema_ptr->end()) {
      // Field exists, check its type.
      auto &field_map = std::get<JsonMap>(*existing_field_iter);
      JsonValue &existing_type = field_map["type"];
      if (!std::holds_alternative<JsonArray>(existing_type)) {
        // If the existing type is not already a JsonArray, make it one with the
        // existing type as its first element.
        existing_type = JsonArray{existing_type};
      }

      //  Add the new type if it's not already present in the array.
      auto &types_array = std::get<JsonArray>(existing_type);
      if (find(types_array.begin(), types_array.end(), JsonValue(type)) ==
          types_array.end()) {
        types_array.emplace_back(type);
      }
    } else {
      // If the array is empty or the last element is not a JsonMap, then add a
      // new map
      current_schema_ptr->emplace_back(
          JsonMap{{"name", current_key}, {"type", type}});
    }
  } else {
    // If there's no current key, we're directly modifying the type of the
    // current schema or object. This part might need clarification, as directly
    // appending types to the schema is unusual. Assuming a direct append to the
    // schema is desired if no current key.
    if (find(current_schema_ptr->begin(), current_schema_ptr->end(),
             JsonValue(type)) == current_schema_ptr->end()) {
      current_schema_ptr->emplace_back(type);
    }
  }
}

bool AvroSchemaHandler::StartArray() {
  JsonMap new_array_items = {{"type", "array"}, {"items", JsonArray{}}};
  JsonArray *new_objects_ptr;
  auto &[current_type, current_schema_ptr, current_prefix, current_key, index] =
      schema_ptr_stack.back();
  index += 1;
  if (!current_key.empty()) {
    current_schema_ptr->emplace_back(
        JsonMap{{"name", current_key}, {"type", new_array_items}});
    new_objects_ptr = &std::get<JsonArray>(std::get<JsonMap>(
        std::get<JsonMap>(current_schema_ptr->back())["type"])["items"]);
  } else {
    current_schema_ptr->emplace_back(new_array_items);
    new_objects_ptr = &std::get<JsonArray>(
        std::get<JsonMap>(current_schema_ptr->back())["items"]);
  }
  //  std::string new_key = create_prefix(current_prefix, current_key, index);
  schema_ptr_stack.emplace_back(JsonType::Array, new_objects_ptr, current_key,
                                "", 0);
  return true;
}

bool AvroSchemaHandler::StartObject() {
  JsonMap new_object = {{"type", "record"}, {"fields", JsonArray{}}};
  JsonArray *new_objects_ptr;
  auto &[current_type, current_schema_ptr, current_prefix, current_key, index] =
      schema_ptr_stack.back();
  index += 1;
  if (!current_key.empty()) {
    new_object["name"] = current_key + "Type";
    current_schema_ptr->emplace_back(
        JsonMap{{"name", current_key}, {"type", new_object}});
    new_objects_ptr = &std::get<JsonArray>(std::get<JsonMap>(
        std::get<JsonMap>(current_schema_ptr->back())["type"])["fields"]);
  } else {
    new_object["name"] = current_prefix + "Type";
    current_schema_ptr->emplace_back(new_object);
    new_objects_ptr = &std::get<JsonArray>(
        std::get<JsonMap>(current_schema_ptr->back())["fields"]);
  }
  //    std::string new_key = create_prefix(current_prefix, current_key, index);
  schema_ptr_stack.emplace_back(JsonType::Record, new_objects_ptr, current_key,
                                "", 0);
  return true;
}

bool AvroSchemaHandler::EndObject(rapidjson::SizeType) {
  schema_ptr_stack.pop_back();
  return true;
}

bool AvroSchemaHandler::EndArray(rapidjson::SizeType) {
  auto &[current_type, current_schema_ptr, current_prefix, current_key, index] =
      schema_ptr_stack.back();

  if (current_schema_ptr->empty()) {
    current_schema_ptr->emplace_back("null");
    current_schema_ptr->emplace_back("string");
    schema_ptr_stack.pop_back();
    return true;
  }

  create_union_types(current_schema_ptr);

  schema_ptr_stack.pop_back();

  return true;
}

void AvroSchemaHandler::recursive_update(JsonValue *d, const JsonValue &u) {
  // Safe to proceed since both are JsonMaps
  auto dMap = std::get<JsonMap>(*d);
  const auto &uMap = std::get<JsonMap>(u);

  for (auto [k, v] : uMap) {
    if (dMap.find(k) == dMap.end()) {
      (dMap)[k] = v;
      continue;
    }
    if (std::holds_alternative<JsonMap>(v)) {
      if (std::holds_alternative<JsonMap>((dMap)[k])) {
        recursive_update(&(dMap)[k], std::get<JsonMap>(v));
        continue;
      }
    }

    if (std::holds_alternative<JsonArray>(v)) {
      set_compatibility(&std::get<JsonArray>((dMap)[k]),
                        &std::get<JsonArray>(v));
      set_compatibility(&std::get<JsonArray>(v),
                        &std::get<JsonArray>((dMap)[k]));
      std::get<JsonArray>((dMap)[k]).insert(
          std::get<JsonArray>((dMap)[k]).end(), std::get<JsonArray>(v).begin(),
          std::get<JsonArray>(v).end());
      create_union_types(&std::get<JsonArray>((dMap)[k]));
      continue;
    }

    (dMap)[k] = v;  // fallback replace
  }
}

void AvroSchemaHandler::set_compatibility(JsonArray *items1,
                                          JsonArray *items2) {
  JsonArray new_items;
  // forward_compatibility
  for (auto item : *items1) {
    // backward compatibility
    if (!exists_in_array(*items2, item)) {
      auto *itemMap = &std::get<JsonMap>(
          item);  // Direct reference to the map in the variant
      (*itemMap)["default"] = nullptr;

      if (std::holds_alternative<JsonMap>((*itemMap)["type"]) ||
          std::holds_alternative<std::string>((*itemMap)["type"])) {
        (*itemMap)["type"] = JsonArray{"null", (*itemMap)["type"]};
        new_items.emplace_back(item);
        continue;
      }
      if (std::holds_alternative<JsonArray>((*itemMap)["type"])) {
        bool null_exists = false;
        for (const auto &type : std::get<JsonArray>((*itemMap)["type"])) {
          if (type == JsonValue("null")) {
            null_exists = true;
            break;
          }
        }
        if (!null_exists) {
          std::get<JsonArray>((*itemMap)["type"]).emplace_back("null");
        }
        continue;
      }
    }
    new_items.emplace_back(item);
  }
  (*items1) = new_items;
}

bool AvroSchemaHandler::exists_in_array(const JsonArray &array,
                                        const JsonValue &item) {
  return std::any_of(
      array.begin(), array.end(), [&item](const JsonValue &arrayItem) {
        if (std::holds_alternative<JsonMap>(item) &&
            std::holds_alternative<JsonMap>(arrayItem)) {
          const auto &itemMap = std::get<JsonMap>(item);
          const auto &arrayItemMap = std::get<JsonMap>(arrayItem);
          // compare the "name" field of the map
          if (itemMap.find("name") != itemMap.end() &&
              arrayItemMap.find("name") != arrayItemMap.end()) {
            return itemMap.at("name") == arrayItemMap.at("name");
          }
        }
        // Fallback for simple types or to handle other complex types
        return item == arrayItem;
      });
}

std::pair<std::string, std::string> AvroSchemaHandler::get_type(
    const JsonValue &item) {
  if (std::holds_alternative<std::string>(item)) {
    return {"", std::get<std::string>(item)};
  }

  std::string name;
  std::string type("string");
  if (std::holds_alternative<JsonMap>(item)) {
    auto &map = std::get<JsonMap>(item);
    if (map.find("name") != map.end()) {
      if (std::holds_alternative<std::string>(map.at("name"))) {
        name = std::get<std::string>(map.at("name"));
      }
    }
    if (map.find("type") != map.end()) {
      if (std::holds_alternative<std::string>(map.at("type"))) {
        type = std::get<std::string>(map.at("type"));
      }
      if (std::holds_alternative<JsonArray>(map.at("type"))) {
        type = "union";
      }
      if (std::holds_alternative<JsonMap>(map.at("type")) &&
          std::get<JsonMap>(map.at("type")).find("type") !=
              std::get<JsonMap>(map.at("type")).end()) {
        type =
            std::get<std::string>(std::get<JsonMap>(map.at("type")).at("type"));
      }
    }
  }
  return {name, type};  // basic type
}

void AvroSchemaHandler::create_union_types(JsonArray *items) {
  JsonMap union_types;
  std::unordered_set<std::string> types;
  //  union_types["array"] = JsonMap{};   // general array
  //  union_types["record"] = JsonMap{};  // general record
  //  union_types["union"] = JsonMap{};   // general union
  LOG << "start union type creation";
  LOG << "current schema: " << py::str(parse_json_value(schema[0]));
  LOG << "items: " << py::str(parse_json_value(*items));
  for (auto item : *items) {
    auto [name, type] = get_type(item);
    if (name == "metric") {
      std::cout << "metric: " << py::str(parse_json_value(item)) << std::endl;
    }
    types.insert(type);

    if (name.empty()) {
      name = type;
    }
    // implement a recursive merge if the type is union
    if (union_types.find(name) == union_types.end()) {
      union_types[name] = item;
      continue;
    }
    auto [previous_name, previous_type] = get_type(union_types[name]);
    JsonValue *previous_item = &union_types[name];

    if (name == "metric") {
      std::cout << "metric: " << py::str(parse_json_value(item)) << std::endl;
      std::cout << "dMap: " << py::str(parse_json_value(*previous_item))
                << std::endl;
    }
    if (previous_type != type && type != "record" && type != "array" &&
        type != "union") {
      std::get<JsonMap>(*previous_item)["type"] =
          JsonArray{union_types[name], type};
    }

    if (type == "record") {
      recursive_update(previous_item, item);
    }

    if (type == "array") {
      if (type == name) {
        auto &previous_items =
            std::get<JsonArray>(std::get<JsonMap>(*previous_item)["items"]);
        JsonArray new_items =
            std::get<JsonArray>(std::get<JsonMap>(item)["items"]);
        previous_items.insert(previous_items.end(), new_items.begin(),
                              new_items.end());
        continue;
      }
      recursive_update(previous_item, item);
    }
  }

  std::cout << "union_types: " << py::str(parse_json_value(union_types))
            << std::endl;

  JsonArray union_items;
  for (const auto &[name, item] : union_types) {
    if ((name == "array" || name == "record" || name == "union") &&
        std::get<JsonMap>(item).empty()) {
      // not complex empty types -> they are merged and added
      continue;
    }
    union_items.emplace_back(item);
  }

  std::cout << "end union type creation\n" << std::endl;
  std::cout << "items: " << py::str(parse_json_value(union_items)) << std::endl;
  items = &union_items;
}

//    if (type != name && (type == "record" || type == "union")) {
//
//      JsonValue* current_type = &std::get<JsonMap>(item)["type"];
//      JsonValue* previous_type =
//      &std::get<JsonMap>(union_types[name])["type"];
//
//      // if the previous type and the current type are both records with an
//      JsonMap type, then set_compatibility for the fields
//        if (type == "record" &&
//        std::holds_alternative<JsonMap>(std::get<JsonMap>(union_types[name])["type"]))
//        {
//            JsonArray* current_fields =
//            &std::get<JsonArray>(std::get<JsonMap>(std::get<JsonMap>(item)["type"])["fields"]);
//            JsonArray* previous_fields =
//            &std::get<JsonArray>(std::get<JsonMap>(std::get<JsonMap>(union_types[name])["type"])["fields"]);
//            set_compatibility(previous_fields, current_fields);
//            set_compatibility(current_fields, previous_fields);
//        }
//
//      if (type == "record" &&
//          std::holds_alternative<JsonArray>(*previous_type)) {
//
//        // previous type is a union -> add the new type to the union
//        std::get<JsonArray>(*previous_type).emplace_back(*current_type);
//        create_union_types(std::get<JsonArray>(*previous_type));
//      }
//
//      if (type == "union" && std::holds_alternative<JsonMap>(*previous_type))
//      {
//        // previous type is a union -> add the new type to the union
//        std::get<JsonArray>(*current_type).emplace_back(*previous_type);
//        create_union_types(std::get<JsonArray>(*current_type));
//      }
//
//      // merge the records
//      recursive_update(union_types[name], item);
//      continue;
//    }
//
//    if (type == "array") {
//      set_compatibility(&std::get<JsonArray>(std::get<JsonMap>(union_types[name])["items"]),
//                        &std::get<JsonArray>(std::get<JsonMap>(item)["items"]));
//      set_compatibility(&std::get<JsonArray>(std::get<JsonMap>(item)["items"]),
//                          &std::get<JsonArray>(std::get<JsonMap>(union_types[name])["items"]));
//      recursive_update(union_types[name], item);
//      continue;
//    }

//      if (std::get<JsonMap>(item).find("items") !=
//          std::get<JsonMap>(item).end()) {
//        JsonMap *old_item_map = type != name
//                                ? &std::get<JsonMap>(union_types[name])
//                                    :
//                                    &std::get<JsonMap>(union_types["array"]);
//        JsonMap item_map = std::get<JsonMap>(item);
//        bool flat_items =
//            std::holds_alternative<std::string>(item_map["items"]);
//        JsonArray old_item_array =
//            old_item_map->find("items") != old_item_map->end()
//                ? std::get<JsonArray>(old_item_map->at("items"))
//                : JsonArray{};
//        JsonArray nested_items =
//            flat_items ? JsonArray{std::get<std::string>(item_map["items"])}
//                       : std::get<JsonArray>(item_map["items"]);
//        nested_items.insert(nested_items.end(), old_item_array.begin(),
//                            old_item_array.end());
//        create_union_types(nested_items);
//    if (get_type(union_types[name]).second != type) {
//      // check if the current type is a string but not equals the current type
//      if (std::holds_alternative<JsonMap>(union_types[name]) &&
//          std::get<JsonMap>(union_types[name]).find("type") !=
//              std::get<JsonMap>(union_types[name]).end()) {
//        if (std::holds_alternative<std::string>(
//                std::get<JsonMap>(union_types[name])["type"])) {
//          std::get<JsonMap>(union_types[name])["type"] =
//              JsonArray{std::get<JsonMap>(union_types[name])["type"], type};
//        } else if (std::holds_alternative<JsonArray>(
//                       std::get<JsonMap>(union_types[name])["type"])) {
//          // check if the current type is not in the old type array
//          for (const auto &old_type : std::get<JsonArray>(
//                   std::get<JsonMap>(union_types[name])["type"])) {
//            if (std::get<std::string>(old_type) == type) {
//              continue;
//            }
//          }
//          std::get<JsonArray>(std::get<JsonMap>(union_types[name])["type"])
//              .emplace_back(type);
//        }
//      }
//      continue;
//    }
//  }
//  if (!std::get<JsonMap>(union_types["array"]).empty()) {
//    union_items.emplace_back(union_types["array"]);
//  }
bool AvroSchemaHandler::Key(const char *str, rapidjson::SizeType length,
                            bool copy) {
  schema_ptr_stack.back().key = std::string(str, length);
  return true;
}

bool AvroSchemaHandler::String(const char *str, rapidjson::SizeType length,
                               bool copy) {
  set_type("string");
  return true;
}

bool AvroSchemaHandler::Int(int i) {
  set_type("int");
  return true;
}

bool AvroSchemaHandler::Uint(unsigned u) {
  set_type("int");
  return true;
}

bool AvroSchemaHandler::Double(double d) {
  set_type("double");
  return true;
}

bool AvroSchemaHandler::Int64(int64_t i) {
  set_type("int");
  return true;
}

bool AvroSchemaHandler::Uint64(uint64_t u) {
  set_type("int");
  return true;
}

bool AvroSchemaHandler::Null() {
  set_type("null");
  return true;
}

bool AvroSchemaHandler::Bool(bool b) {
  set_type("boolean");
  return true;
}

bool AvroSchemaHandler::RawNumber(const char *str, rapidjson::SizeType length,
                                  bool copy) {
  set_type("long");
  return true;
}

py::object JsonValueVisitor::operator()(const JsonMap &map) const {
  if (map.empty()) {
    return py::none();
  }
  py::dict py_map;
  for (const auto &[key, value] : map) {
    py_map[py::cast(key)] = std::visit(JsonValueVisitor(), value);
  }
  return py_map;
}

py::object JsonValueVisitor::operator()(const JsonArray &array) const {
  if (array.size() == 1 && std::holds_alternative<std::string>(array[0])) {
    return std::visit(JsonValueVisitor(), array[0]);
  }
  py::list py_list;
  for (const auto &value : array) {
    py_list.append(std::visit(JsonValueVisitor(), value));
  }
  return py_list;
}

py::object JsonValueVisitor::operator()(nullptr_t) const { return py::none(); }

py::object JsonValueVisitor::operator()(bool b) const { return py::bool_(b); }

py::object JsonValueVisitor::operator()(int i) const { return py::int_(i); }

py::object JsonValueVisitor::operator()(unsigned u) const {
  return py::int_(u);
}

py::object JsonValueVisitor::operator()(int64_t i) const { return py::int_(i); }

py::object JsonValueVisitor::operator()(uint64_t u) const {
  return py::int_(u);
}

py::object JsonValueVisitor::operator()(double d) const {
  return py::float_(d);
}

py::object JsonValueVisitor::operator()(const std::string &s) const {
  return py::str(s);
}

py::object JsonValueVisitor::operator()(const py::object &obj) const {
  return obj;
}

py::object parse_json_value(const JsonValue &value) {
  if (std::variant(value).valueless_by_exception()) {
    return py::none();
  }
  return std::visit(JsonValueVisitor(), value);
}

JsonValue PythonDictVisitor::operator()(const py::object &obj) const {
  if (py::isinstance<py::dict>(obj)) {
    return visit_dict(py::cast<py::dict>(obj));
  } else if (py::isinstance<py::list>(obj)) {
    return visit_list(py::cast<py::list>(obj));
  } else if (py::isinstance<py::none>(obj)) {
    return visit_none();
  } else if (py::isinstance<py::bool_>(obj)) {
    return visit_bool(py::cast<py::bool_>(obj));
  } else if (py::isinstance<py::int_>(obj)) {
    return visit_int(py::cast<py::int_>(obj));
  } else if (py::isinstance<py::float_>(obj)) {
    return visit_float(py::cast<py::float_>(obj));
  } else if (py::isinstance<py::str>(obj)) {
    return visit_str(py::cast<py::str>(obj));
  } else {
    // Fallback for unsupported types
    throw std::runtime_error("Unsupported Python object type");
  }
}

JsonValue PythonDictVisitor::visit_dict(const py::dict &dict) const {
  std::unordered_map<std::string, JsonValue> map;
  for (const auto &item : dict) {
    map[py::cast<std::string>(item.first)] =
        (*this)(py::cast<py::object>(item.second));
  }
  return map;
}

JsonValue PythonDictVisitor::visit_list(const py::list &list) const {
  std::vector<JsonValue> array;
  for (const auto &item : list) {
    array.push_back((*this)(py::cast<py::object>(item)));
  }
  return array;
}

JsonValue PythonDictVisitor::visit_none() { return nullptr; }

JsonValue PythonDictVisitor::visit_bool(const py::bool_ &b) {
  return b.cast<bool>();
}

JsonValue PythonDictVisitor::visit_int(const py::int_ &i) {
  return i.cast<int>();
}

JsonValue PythonDictVisitor::visit_float(const py::float_ &f) {
  return f.cast<double>();
}

JsonValue PythonDictVisitor::visit_str(const py::str &s) {
  return s.cast<std::string>();
}

JsonValue parse_python_dict(const py::dict &obj) {
  PythonDictVisitor visitor;
  return visitor(obj);
}

}  // namespace json
