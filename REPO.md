Activities and Lessons Learned:

5 Fuzzed Functions:
After fuzzing the keyMiner function we made 3 main fixes
    It now correctly returns the index of a value in a list as a string.

    The function stops searching as soon as it finds the value, making it more efficient.

    The function no longer includes the value itself in the result, only the path to it.

After fuzzing the getKeyRecursively function we made 1 main fix
    It now includes keys with empty lists or empty dictionaries instead of skipping them

After fuzzing the getValueRecursively function we did not run into any errors so there were no major fixes we had to make
