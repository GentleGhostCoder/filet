# Makefile for building and running tests with Catch2
# Compiler settings
CXX = g++
CXXFLAGS = -Wall -std=c++11

# Directories
SRC_DIR = ./
LIB_DIR = ../lib
CATCH_DIR = $(LIB_DIR)/catch2/target/include
RAPIDJSON_DIR = $(LIB_DIR)/rapidjson/include
INCLUDE = -I$(SRC_DIR) -I$(LIB_DIR) -I$(RAPIDJSON_DIR) -I$(CATCH_DIR)

# Source and target settings
SRC = test_eval_json.cpp
OBJ = $(SRC:.cpp=.o)
TARGET = run_tests

# Default target
all: $(TARGET)

$(TARGET): $(OBJ)
	$(CXX) $(CXXFLAGS) $(INCLUDE) -o $@ $^

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDE) -c $< -o $@

# Run tests
test: $(TARGET)
	./$(TARGET)

# Clean up
clean:
	rm -f $(OBJ) $(TARGET)

.PHONY: all test clean
