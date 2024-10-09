// Copyright (c) 2024 Semjon Geist.
#include <bindings.hpp>

//! pybind module declaration
PYBIND11_MODULE(_cpputils, module) {
  module.doc() = R"pbdoc(
        filet.cpputils (Pybind11 modules)
        ------------------------------
        .. currentmodule:: filet._cpputils

        .. autosummary::
           :toctree: _generate

            eval_type
            eval_datetime
            eval_csv
            JsonHandler
            AvroSchemaHandler
            FlatJsonHandler
    )pbdoc";

  py::class_<json::JsonHandler, json::PyJsonFlattenHandler>(module,
                                                            "JsonHandler")
      .def(py::init<>())
      .def("StartObject", &json::JsonHandler::StartObject)
      .def("EndObject", &json::JsonHandler::EndObject)
      .def("StartArray", &json::JsonHandler::StartArray)
      .def("EndArray", &json::JsonHandler::EndArray)
      .def("Key", &json::JsonHandler::Key)
      .def("String", &json::JsonHandler::String)
      .def("Int", &json::JsonHandler::Int)
      .def("Uint", &json::JsonHandler::Uint)
      .def("Bool", &json::JsonHandler::Bool)
      .def("Null", &json::JsonHandler::Null)
      .def("Double", &json::JsonHandler::Double)
      .def("Int64", &json::JsonHandler::Int64)
      .def("Uint64", &json::JsonHandler::Uint64)
      .def("RawNumber", &json::JsonHandler::RawNumber)
      .def("parse_json_bytes", &json::JsonHandler::parse_json_bytes);

  py::class_<json::AvroSchemaHandler, json::JsonHandler>(module,
                                                         "AvroSchemaHandler")
      .def(py::init<>())  // Bind the constructor
      .def("create_schema", &json::AvroSchemaHandler::create_schema)
      .def("read_existing_schema",
           &json::AvroSchemaHandler::read_existing_schema)
      .def("update_schema", &json::AvroSchemaHandler::update_schema)
      .def("get_schema", &json::AvroSchemaHandler::get_schema);

  py::class_<json::FlatJsonHandler, json::JsonHandler>(module,
                                                       "FlatJsonHandler")
      .def(py::init<>())  // Bind the constructor
      .def("loads", &json::FlatJsonHandler::loads)
      .def("header", &json::FlatJsonHandler::header);

  module.def(
      "eval_type",
      [](const std::string &value) -> py::object {
        return string_operations::eval_type(value);
      },
      py::arg("value").none(false),
      R"pbdoc(
        .. doxygenfunction:: string_operations::eval_type
            :project: filet.cpputils
        )pbdoc");

  module.def(
      "eval_datetime",
      [](const std::string &value) -> py::object {
        return string_operations::eval_datetime(value);
      },
      py::arg("value").none(false),
      R"pbdoc(
        .. doxygenfunction:: string_operations::eval_datetime
            :project: filet.cpputils
        )pbdoc");

  module.def(
      "eval_csv",
      [](const std::string &value,
         const char *disallowed_header_chars) -> py::object {
        if (value.empty()) {
          py::object logger = py::module::import("logging");
          logger.attr("error")("Can´t evaluate empty csv value!");
          return py::none();
        }
        return py::cast(
            string_operations::eval_csv(value, disallowed_header_chars));
      },
      py::arg("value").none(false), py::arg("disallowed_header_chars") = "",
      R"pbdoc(
        .. doxygenfunction:: string_operations::eval_csv
            :project: filet.cpputils
        )pbdoc");

  module.attr("__name__") = "filet.cpputils";
#ifdef VERSION_INFO
  module.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
  module.attr("__version__") = "dev";
#endif
}
