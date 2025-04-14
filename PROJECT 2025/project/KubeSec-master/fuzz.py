from parser import keyMiner
from parser import getKeyRecursively
from parser import getValuesRecursively
from parser import getValsFromKey
from parser import checkIfValidHelm

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

def fuzz_getValsFromKey():
    test_cases = [
        # Test 1: Simple top-level key match
        {"data": {"a": 1, "b": 2}, "target": "a", "expected": [1]},

        # Test 2: Deeply nested target key
        {"data": {"a": {"b": {"c": 3}}}, "target": "c", "expected": [3]},

        # Test 3: Target key appears multiple times in a list
        {"data": {"a": [{"b": 1}, {"b": 2}]}, "target": "b", "expected": [1, 2]},

        # Test 4: Target key inside a list within a dictionary
        {"data": {"x": {"y": [1, {"z": 42}]}}, "target": "z", "expected": [42]},

        # Test 5: Very deep nested key path
        {"data": {"a": {"b": {"c": {"d": {"e": 5}}}}}, "target": "e", "expected": [5]},

        # Test 6: No match found
        {"data": {}, "target": "foo", "expected": []},

        # Test 7: Same key appears at two levels
        {"data": {"a": 1, "b": 2, "c": {"a": 3}}, "target": "a", "expected": [1, 3]},

        # Test 8: Repeated target keys in a list of dictionaries
        {"data": {"list": [{"target": 1}, {"target": 2}, {"target": 3}]}, "target": "target", "expected": [1, 2, 3]},

        # Test 9: Target key deeply nested
        {"data": {"outer": {"inner": {"deep": {"target": 9}}}}, "target": "target", "expected": [9]},

        # Test 10: None as value, but key still matches
        {"data": {"a": None, "b": {"a": "value"}}, "target": "a", "expected": [None, "value"]},
    ]
    for i, case in enumerate(test_cases):
        print(f"[getValsFromKey] Test Case {i + 1}")
        try:
            result_holder = []
            getValsFromKey(case["data"], case["target"], result_holder)
            print("Result:", result_holder)
            assert result_holder == case["expected"], f"Failed: Expected {case['expected']}, got {result_holder}"
            print("Test Passed\n")
        except Exception as e:
            print(f"Error: {e}\n")
        print("-" * 50)

def fuzz_checkIfValidHelm():
    test_cases = [
        # Test 1: Common Helm file name
        {"input": "values.yaml", "expected": True},

        # Test 2: Template file used in Helm charts
        {"input": "templates/deployment.yaml", "expected": True},

        # Test 3: Service file under a chart folder
        {"input": "charts/service.yaml", "expected": True},

        # Test 4: Unrelated file name
        {"input": "somefolder/nonsensicalfile.txt", "expected": False},

        # Test 5: Configuration file inside chart
        {"input": "charts/mychart/config.yaml", "expected": True},

        # Test 6: Helm-specific filename
        {"input": "helmfile.yaml", "expected": True},

        # Test 7: YAML file not related to Helm
        {"input": "config-notrelated.yml", "expected": False},

        # Test 8: Helm values file with long name
        {"input": "deployments/helm-service-values.yaml", "expected": True},

        # Test 9: Service and ingress in name
        {"input": "manifests/service-ingress-chart.yaml", "expected": True},

        # Test 10: Simple unrelated YAML
        {"input": "foo/bar.yaml", "expected": False},
    ]
    for i, case in enumerate(test_cases):
        print(f"[checkIfValidHelm] Test Case {i + 1}")
        try:
            result = checkIfValidHelm(case["input"])
            print("Result:", result)
            assert result == case["expected"], f"Failed: Expected {case['expected']}, got {result}"
            print("Test Passed\n")
        except Exception as e:
            print(f"Error: {e}\n")
        print("-" * 50)


# Call the fuzzing functions
#Test 1: fuzz_keyMiner()
print("KeyMiner Fuzzing\n")
fuzz_keyMiner()
print("\n---------------------------------------------------------------\n")
print("-----------------------------------------------------------------\n")

#Test 2: fuzz_getKeyRecursively()
print("GetKeyRecursively Fuzzing\n")
fuzz_getKeyRecursively()
print("\n---------------------------------------------------------------\n")
print("-----------------------------------------------------------------\n")

#Test 3: fuzz_getValuesRecursivly()
print("GetValuesRecursively Fuzzing\n")
fuzz_getValuesRecursively()
print("\n---------------------------------------------------------------\n")
print("-----------------------------------------------------------------\n")

##Test 4: fuzz_getValsFromKey()
print("GetValsFromKey Fuzzing\n")
fuzz_getValsFromKey()
print("\n---------------------------------------------------------------\n")
print("-----------------------------------------------------------------\n")

#Test 5: fuzz_checkIfValidHelm()
print("CheckIfValidHelm Fuzzing\n")
fuzz_checkIfValidHelm()
print("\n---------------------------------------------------------------\n")
print("-----------------------------------------------------------------\n")
