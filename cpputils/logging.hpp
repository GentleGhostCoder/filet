// Copyright (c) 2024 Semjon Geist.

//
// Created by sgeist on 16.02.24.
//

#ifndef CPPUTILS_LOGGING_HPP_
#define CPPUTILS_LOGGING_HPP_

#include <iostream>
#include <sstream>

// Logger class declaration
class Logger {
 public:
  Logger() = default;

  // Destructor appends std::endl automatically
  ~Logger() {
#ifdef DEBUG_MODE
    std::cout << std::endl;
#endif
  }

  // Overload the << operator for various types
  template <typename T>
  Logger& operator<<(const T& val) {
#ifdef DEBUG_MODE
    std::cout << val;
#endif
    return *this;
  }
};

// Macro to create a temporary Logger object
#define LOG Logger()

#endif  // CPPUTILS_LOGGING_HPP_
