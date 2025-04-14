Activities and Lessons Learned:

5 Fuzzed Functions:
After fuzzing the keyMiner function we made 3 main fixes
    It now correctly returns the index of a value in a list as a string.

    The function stops searching as soon as it finds the value, making it more efficient.

    The function no longer includes the value itself in the result, only the path to it.

After fuzzing the getKeyRecursively function we made 1 main fix
    It now includes keys with empty lists or empty dictionaries instead of skipping them

After fuzzing the getValueRecursively function we did not run into any errors so there were no major fixes we had to make

After fuzzing the getValsFromKey function we found bugs: tt failed to detect keys that were nested inside list elements and that it included empty dictionary values like {} as valid matches.
    Updated: the recursion logic to handle both lists and dicts properly and  added a condition to skip empty dictionaries before appending results

After fuzzing the checkIfValidHelm function we found it did not detect common Helm-related files such as "values.yaml" and "helmfile.yaml".
    Updated: added case-insensitive matching and explicitly checked for known filenames

