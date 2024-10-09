// Copyright (c) 2024 Semjon Geist.
//
// Created by sgeist on 14.02.24.
//
#include <string_operations.hpp>

namespace string_operations {

std::map<std::string, py::object> eval_csv(
    const std::string &input, const char *extra_disallowed_header_chars = "") {
  std::map<std::string, py::object> format;

  // Detect line separator
  std::vector<std::string> line_separators = {"\r\n", "\r", "\n"};
  std::string line_separator;
  for (const auto &sep : line_separators) {
    if (input.find(sep) != std::string::npos) {
      line_separator = sep;
      break;
    }
  }
  format["line_separator"] = py::cast(line_separator);

  // Split input into lines
  std::vector<std::string> lines;
  std::stringstream ss(input);
  std::string line;
  while (std::getline(ss, line, line_separator[0])) {
    lines.push_back(line);
  }

  format["parsed_line_count"] = py::cast(lines.size());

  // Detect column separator and quoting character
  std::vector<std::string> column_separators = {",", ";", "\t", "|", "\b"};
  std::string column_separator, quoting_character;
  for (const auto &sep : column_separators) {
    if (lines[0].find(sep) != std::string::npos) {
      column_separator = sep;
      break;
    }
  }
  format["column_separator"] = py::cast(column_separator);

  // Detect header
  std::vector<std::string> header;
  std::vector<std::string> column_types;
  bool has_header = true;
  std::stringstream line_stream(lines[0]);
  std::string cell;
  while (std::getline(line_stream, cell, column_separator[0])) {
    if ((!cell.empty() && !is_nan(cell) &&
         (cell[0] == QUOTE_CHARS[0] || cell[0] == QUOTE_CHARS[1]) &&
         (!is_quoted(cell[0], cell.back()) ||
          !(is_quoted(cell[0], cell.back()) &&
            std::count(cell.begin(), cell.end(), cell[0]) % 2 == 0))) ||
        (cell.length() == 1 &&
         (cell[0] == QUOTE_CHARS[0] || cell[0] == QUOTE_CHARS[1]))) {
      std::string full_cell = cell;
      quoting_character = cell[0];
      while (std::getline(line_stream, cell, column_separator[0])) {
        full_cell.append(column_separator[0] + cell);
        if (!cell.empty() &&
            (cell.back() == QUOTE_CHARS[0] || cell.back() == QUOTE_CHARS[1]) &&
            std::count(full_cell.begin(), full_cell.end(), full_cell[0]) % 2 ==
                0) {
          break;
        }
      }
      cell = full_cell;
    }
    if (!cell.empty() && is_quoted(cell[0], cell.back())) {
      cell = cell.erase(0, 1).erase(cell.size() - 1);
    }
    header.push_back(cell);
  }

  for (const auto &h : header) {
    column_types.push_back(
        eval_type(h).attr("__class__").attr("__name__").cast<std::string>());
    if (column_types.back() == "NoneType") {
      continue;
    }
    if (column_types.back() != "str" ||
        h.find_first_of(SPECIAL_CHARS + extra_disallowed_header_chars) !=
            std::string::npos ||
        h.empty()) {
      has_header = false;
    }
  }
  format["has_header"] = py::cast(has_header);
  if (has_header) {
    format["header"] = py::cast(header);
    column_types.clear();
  }

  for (auto it = std::next(lines.begin()); it != lines.end(); ++it) {
    int col_idx = 0;
    line = *it;
    std::stringstream l_stream(line);
    while (std::getline(l_stream, cell, column_separator[0])) {
      if ((!cell.empty() && !is_nan(cell) &&
           (cell[0] == QUOTE_CHARS[0] || cell[0] == QUOTE_CHARS[1]) &&
           (!is_quoted(cell[0], cell.back()) ||
            !(is_quoted(cell[0], cell.back()) &&
              std::count(cell.begin(), cell.end(), cell[0]) % 2 == 0))) ||
          (cell.length() == 1 &&
           (cell[0] == QUOTE_CHARS[0] || cell[0] == QUOTE_CHARS[1]))) {
        std::string full_cell = cell;
        quoting_character = cell[0];
        while (std::getline(l_stream, cell, column_separator[0])) {
          full_cell.append(column_separator[0] + cell);
          if (!cell.empty() &&
              (cell.back() == QUOTE_CHARS[0] ||
               cell.back() == QUOTE_CHARS[1]) &&
              std::count(full_cell.begin(), full_cell.end(), full_cell[0]) %
                      2 ==
                  0) {
            break;
          }
        }
        cell = full_cell;
      }
      if (col_idx < static_cast<int>(column_types.size()) &&
          !is_nan(column_types[col_idx])) {
        col_idx++;
        continue;
      }
      if ((col_idx >= static_cast<int>(column_types.size())) != 0) {
        if (cell.empty() || is_nan(cell)) {
          column_types.emplace_back("NoneType");
          if (col_idx >= static_cast<int>(column_types.size())) {
            header.emplace_back("");  // fill header
          }
          col_idx++;
          continue;
        }
        column_types.push_back(eval_type(cell)
                                   .attr("__class__")
                                   .attr("__name__")
                                   .cast<std::string>());
        if (col_idx >= static_cast<int>(column_types.size())) {
          header.emplace_back("");  // fill header
        }
        col_idx++;
        continue;
      }
      if (!cell.empty() && !is_nan(cell)) {
        auto cell_type = eval_type(cell)
                             .attr("__class__")
                             .attr("__name__")
                             .cast<std::string>();
        column_types[col_idx] = cell_type;
      }
      col_idx++;
    }
  }
  format["column_types"] = py::cast(column_types);
  format["column_count"] =
      py::cast(!column_types.empty() ? column_types.size() : header.size());
  format["quoting_character"] = py::cast(quoting_character);
  return format;
}
}  // namespace string_operations
