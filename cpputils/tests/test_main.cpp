// Copyright (c) 2024 Semjon Geist.

//
// Created by sgeist on 12.02.24.
//
#include <tests/catch2.hpp>

// main
int main(int argc, char *argv[]) {
  Catch::Session session;
  int result = session.applyCommandLine(argc, argv);
  if (result != 0) {
    return result;
  }
  result = session.run();
  return result;
}
