// Copyright (c) 2024 Semjon Geist.
#ifndef CPPUTILS_BINDINGS_HPP_
#define CPPUTILS_BINDINGS_HPP_

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

// clang-format off
#include <string>
#include <vector>
#include <numeric>
#include <iomanip>
#include <eval_json.hpp>
// clang-format on

namespace py = pybind11;
#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

#endif  // CPPUTILS_BINDINGS_HPP_
