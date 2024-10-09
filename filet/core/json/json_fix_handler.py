from filet.cpputils import JsonHandler


class JsonFixHandler(JsonHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rebuilt_json = ""
        self.depth_stack = []
        self.element_added = []
        self.expecting_value = False

    def StartObject(self):
        self.maybeAddComma()
        self.rebuilt_json += "{"
        self.depth_stack.append("}")
        self.element_added.append(False)
        self.expecting_value = False  # Reset expectation for new object
        return True

    def EndObject(self, elementCount):
        self.addValueIfNeeded()  # Add default value if a key was last without a value
        self.rebuilt_json += "}"
        self.depth_stack.pop()
        self.element_added.pop()
        self.finalizeStructure()
        return True

    def StartArray(self):
        self.maybeAddComma()
        self.rebuilt_json += "["
        self.depth_stack.append("]")
        self.element_added.append(False)
        self.expecting_value = False  # Reset expectation for new array
        return True

    def EndArray(self, elementCount):
        self.rebuilt_json += "]"
        self.depth_stack.pop()
        self.element_added.pop()
        self.finalizeStructure()
        return True

    def Key(self, key, length, copy):
        self.addValueIfNeeded()  # Add default value if a previous key was without a value
        self.maybeAddComma()
        self.rebuilt_json += f'"{key}":'
        self.expecting_value = True  # Now expecting a value
        self.element_added[-1] = False  # Mark as not added because we're waiting for the value
        return True

    def maybeAddComma(self):
        if self.element_added and self.element_added[-1]:
            self.rebuilt_json += ","

    def addValue(self, value):
        """Helper method to add a value, taking care of commas."""
        self.maybeAddComma()
        self.rebuilt_json += value
        if self.depth_stack:  # Mark that an element has been added to the current structure
            self.element_added[-1] = True
        self.expecting_value = False

    def addValueIfNeeded(self):
        # If we were expecting a value but didn't get one, insert a default value
        if self.expecting_value:
            self.rebuilt_json += "null"  # Or any appropriate default value
            self.expecting_value = False

    # Update all value methods (String, Number, Boolean, Null, etc.) to reset expecting_value
    def String(self, value, length, copy):
        self.addValue(f'"{value}"')
        return True

    def Number(self, value):
        self.addValue(str(value))
        return True

    def Int(self, value):
        self.addValue(str(value))
        return True

    def Double(self, value):
        self.addValue(str(value))
        return True

    def Boolean(self, value):
        self.addValue(str(value).lower())
        return True

    def Null(self):
        self.addValue("null")
        return True

    def RawNumber(self, value, length, copy):
        self.addValue(value)
        return True

    def Uint(self, value):
        self.addValue(str(value))
        return True

    def Int64(self, value):
        self.addValue(str(value))
        return True

    def Uint64(self, value):
        self.addValue(str(value))
        return True

    def finalizeStructure(self):
        # When finishing a structure, mark parent as having an element and reset expectation
        if self.depth_stack:
            self.element_added[-1] = True
        self.expecting_value = False

    def fix_json(self, json_str):
        # clear all the variables
        self.__init__()
        self.parse_json_bytes(json_str)  # Start the parsing process
        self.addValueIfNeeded()  # Ensure we add a value if the JSON ends unexpectedly
        while self.depth_stack:  # Close any unclosed structures
            self.rebuilt_json += self.depth_stack.pop()
        return self.rebuilt_json
