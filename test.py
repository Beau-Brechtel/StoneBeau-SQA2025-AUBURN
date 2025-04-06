# test.py
import pickle
import os

def insecure_function():
    # Insecure use of pickle
    data = pickle.loads("malicious_data")
    return data

def run_command():
    # Insecure use of os.system
    os.system("rm -rf /")