// Copyright (c) 2024 Semjon Geist.

#include <string_operations.hpp>

//! implementations for string operations
namespace string_operations {

bool is_nan(std::string value) {
  std::transform(value.begin(), value.end(), value.begin(), ::toupper);
  return std::find(NAN_STRINGS.begin(), NAN_STRINGS.end(), value) !=
         NAN_STRINGS.end();
}

bool is_quoted(const char &first_char, const char &last_char) {
  return (first_char == QUOTE_CHARS[0] && last_char == QUOTE_CHARS[0]) ||
         (first_char == QUOTE_CHARS[1] && last_char == QUOTE_CHARS[1]);
}

std::string replace_all(const std::string &data, const std::string &to_search,
                        const std::string &replace_str) {
  std::string replacement = data;
  size_t pos = data.find(to_search);

  while (pos != std::string::npos) {
    replacement.replace(pos, to_search.size(), replace_str);
    pos = replacement.find(to_search, pos + replace_str.size());
  }

  return replacement;
}

std::string trim(const std::string &str, const std::string &whitespace) {
  const auto strBegin = str.find_first_not_of(whitespace);
  if (strBegin == std::string::npos) return "";  // no content

  const auto strEnd = str.find_last_not_of(whitespace);
  const auto strRange = strEnd - strBegin + 1;

  return str.substr(strBegin, strRange);
}

std::uint64_t parse8Chars(const char *string) noexcept {
  std::uint64_t chunk = 0;
  std::memcpy(&chunk, string, sizeof(chunk));

  // 1-byte mask trick (works on 4 pairs of single digits)
  std::uint64_t lower_digits = (chunk & 0x0f000f000f000f00) >> 8;
  std::uint64_t upper_digits = (chunk & 0x000f000f000f000f) * 10;
  chunk = lower_digits + upper_digits;

  // 2-byte mask trick (works on 2 pairs of two digits)
  lower_digits = (chunk & 0x00ff000000ff0000) >> 16;
  upper_digits = (chunk & 0x000000ff000000ff) * 100;
  chunk = lower_digits + upper_digits;

  // 4-byte mask trick (works on pair of four digits)
  lower_digits = (chunk & 0x0000ffff00000000) >> 32;
  upper_digits = (chunk & 0x000000000000ffff) * 10000;
  chunk = lower_digits + upper_digits;

  return chunk;
}

std::uint64_t parse64(std::string_view s) noexcept {
  std::uint64_t upper_digits = parse8Chars(s.data());
  std::uint64_t lower_digits = parse8Chars(s.data() + 8);
  return upper_digits * 100000000 + lower_digits;
}

// clang-format off
void preprocessJsonInPlace(std::string* input) {
  char insideQuote = '\0';  // '\0' means outside any string
  size_t pos = 0;
  while (pos < input->size()) {
    size_t nextQuotePos;
    if (insideQuote) {
      // If inside a string, search for the ending quote
      nextQuotePos = input->find(insideQuote, pos);
      if (nextQuotePos == std::string::npos) {
        break;  // No matching ending quote found
      }
      insideQuote = '\0';  // Found, so now outside any string
    } else {
      // If outside a string, search for the next double quote
      nextQuotePos = input->find('"', pos);
      if (nextQuotePos == std::string::npos) {
        break;  // No more double quotes found
      }
      insideQuote = '"';  // Found, so now inside a string
    }
    pos = nextQuotePos + 1;  // Move past the (last) found quote
  }
}

//// clang-format on

}  // namespace string_operations
