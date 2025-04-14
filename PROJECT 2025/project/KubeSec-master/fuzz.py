from parser import keyMiner
from parser import getKeyRecursively
from parser import getValuesRecursively


def fuzz_keyMiner():
    test_cases = [
        # Case 1: Empty dictionary
        {"data": {}, "target": 42, "expected": None},
        # Case 2: Empty list
        {"data": [], "target": 42, "expected": None},
        # Case 3: Single-level dictionary with target value
        {"data": {"a": 42, "b": 100}, "target": 42, "expected": ["a"]},
        # Case 4: Single-level list with target value
        {"data": [1, 2, 42, 4], "target": 42, "expected": ["2"]},
        # Case 5: Nested dictionary with target value
        {"data": {"a": {"b": {"c": 42}}}, "target": 42, "expected": ["a", "b", "c"]},
        # Case 6: Nested list with target value
        {"data": [[1, 2], [3, [4, 42]]], "target": 42, "expected": ["1", "1", "1"]},
        # Case 7: Mixed dictionary and list
        {"data": {"a": [1, {"b": 42}]}, "target": 42, "expected": ["a", "1", "b"]},
        # Case 8: Target value not found
        {"data": {"a": {"b": {"c": 100}}}, "target": 42, "expected": None},
        # Case 9: Multiple occurrences of the target value
        {"data": {"a": 42, "b": {"c": 42}}, "target": 42, "expected": ["a"]},  # Stops at the first match
        # Case 10: Target value is `None`
        {"data": {"a": None, "b": {"c": 42}}, "target": None, "expected": ["a"]},
    ]

    for i, case in enumerate(test_cases):
        data = case["data"]
        target = case["target"]
        expected = case["expected"]

        print(f"Test Case {i + 1}:")
        print(f"Data: {data}")
        print(f"Target: {target}")
        print(f"Expected: {expected}")

        try:
            result = keyMiner(data, target)
            print(f"Result: {result}")
            assert result == expected, f"Test Case {i + 1} Failed: Expected {expected}, got {result}"
            print("Test Passed\n")
        except Exception as e:
            print(f"Error: {e}\n")
        print("-" * 50)

def fuzz_getKeyRecursively():
    test_cases = [
        # Case 1: Empty dictionary
        {"data": {}, "expected": []},
        # Case 2: Single-level dictionary
        {"data": {"a": 1, "b": 2}, "expected": [("a", 0), ("b", 0)]},
        # Case 3: Nested dictionary
        {"data": {"a": {"b": {"c": 3}}}, "expected": [("a", 0), ("b", 1), ("c", 2)]},
        # Case 4: Dictionary with a list
        {"data": {"a": [1, {"b": 2}]}, "expected": [("a", 0), ("b", 1)]},
        # Case 5: Mixed dictionary and list
        {"data": {"x": {"y": [1, {"z": 42}]}}, "expected": [("x", 0), ("y", 1), ("z", 2)]},
        # Case 6: Deeply nested dictionary
        {"data": {"a": {"b": {"c": {"d": {"e": 5}}}}}, "expected": [("a", 0), ("b", 1), ("c", 2), ("d", 3), ("e", 4)]},
        # Case 7: Dictionary with non-dictionary/list values
        {"data": {"a": 1, "b": "string", "c": None}, "expected": [("a", 0), ("b", 0), ("c", 0)]},
        # Case 8: Dictionary with empty list and dictionary
        {"data": {"a": [], "b": {}}, "expected": [("a", 0), ("b", 0)]},

        
    ]
    
    for i, case in enumerate(test_cases):
        data = case["data"]
        expected = case["expected"]

        print(f"Test Case {i + 1}:")
        print(f"Data: {data}")
        print(f"Expected: {expected}")

        try:
            result = []
            getKeyRecursively(data, result)
            print(f"Result: {result}")
            assert result == expected, f"Test Case {i + 1} Failed: Expected {expected}, got {result}"
            print("Test Passed\n")
        except Exception as e:
            print(f"Error: {e}\n")
        print("-" * 50)

def fuzz_getValuesRecursively():
    test_cases = [
        # Case 1: Empty dictionary
        {"data": {}, "expected": []},
        # Case 2: Empty list
        {"data": [], "expected": []},
        # Case 3: Single-level dictionary
        {"data": {"a": 1, "b": 2}, "expected": [1, 2]},
        # Case 4: Single-level list
        {"data": [1, 2, 3], "expected": [1, 2, 3]},
        # Case 5: Nested dictionary
        {"data": {"a": {"b": {"c": 3}}}, "expected": [3]},
        # Case 6: Nested list
        {"data": [[1, 2], [3, [4, 5]]], "expected": [1, 2, 3, 4, 5]},
        # Case 7: Mixed dictionary and list
        {"data": {"a": [1, {"b": 2}]}, "expected": [1, 2]},
        # Case 8: Dictionary with non-dictionary/list values
        {"data": {"a": 1, "b": "string", "c": None}, "expected": [1, "string", None]},
        # Case 9: Dictionary with empty list and dictionary
        {"data": {"a": [], "b": {}}, "expected": []},
        # Case 10: Deeply nested dictionary and list
        {"data": {"x": {"y": [1, {"z": [2, 3]}]}}, "expected": [1, 2, 3]},
         # Case 11: Dictionary with mixed key types
        {"data": {"a": 1, 2: {"b": 3}, (4, 5): {"c": 6}}, "expected": [1, 3, 6]},
        # Case 12: Dictionary with deeply nested empty structures
        {"data": {"a": {"b": {"c": {}}}, "d": []}, "expected": []},
        # Case 13: Dictionary with special characters in keys
        {"data": {"a!@#": 1, "b$%^": {"c&*()": 2}}, "expected": [1, 2]},
        # Case 14: Dictionary with very large depth
        {"data": {"a": {"b": {"c": {"d": {"e": {"f": {"g": {"h": {"i": {"j": 10}}}}}}}}}},
         "expected": [10]},
        # Case 15: Dictionary with None as a key
        {"data": {None: {"a": 1}}, "expected": [1]},
        # Case 16: List with mixed types
        {"data": [1, "string", None, {"a": 2}, [3, 4]], "expected": [1, "string", None, 2, 3, 4]},
        # Case 17: List with empty structures
        {"data": [[], {}, [[], {}]], "expected": []},
        # Case 18: Dictionary with boolean values
        {"data": {"a": True, "b": False}, "expected": [True, False]},
        # Case 19: Dictionary with nested lists containing dictionaries
        {"data": {"a": [{"b": 1}, {"c": 2}], "d": [3, {"e": 4}]}, "expected": [1, 2, 3, 4]},
        # Case 20: Empty and Null Values
        {"data": {"a": None, "b": [], "c": {}}, "expected": [None]},
        
    ]

    for i, case in enumerate(test_cases):
        data = case["data"]
        expected = case["expected"]

        print(f"Test Case {i + 1}:")
        print(f"Data: {data}")
        print(f"Expected: {expected}")

        try:
            result = list(getValuesRecursively(data))
            print(f"Result: {result}")
            assert result == expected, f"Test Case {i + 1} Failed: Expected {expected}, got {result}"
            print("Test Passed\n")
        except Exception as e:
            print(f"Error: {e}\n")
        print("-" * 50)


# Call the fuzzing functions
print("KeyMiner Fuzzing\n")
#fuzz_keyMiner()
print("\n---------------------------------------------------------------\n")
print("-----------------------------------------------------------------\n")
print("GetKeyRecursively Fuzzing\n")
#fuzz_getKeyRecursively()
print("\n---------------------------------------------------------------\n")
print("-----------------------------------------------------------------\n")
print("GetValuesRecursively Fuzzing\n")
fuzz_getValuesRecursively()
print("\n---------------------------------------------------------------\n")
print("-----------------------------------------------------------------\n")
