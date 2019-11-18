import pandas as pd
import jsonpickle
import numpy as np
import matplotlib.pyplot as plt
import os, os.path
import dateutil.parser

# Constants

JSON_STATES_FOLDER =  "../tagging_json_states"

# First get all the json states

path = os.getcwd()
files = os.listdir(JSON_STATES_FOLDER)
files_json = [f for f in files if f[-4:] == 'json']
files_json.sort()
print(len(files_json))

# Get the last state for testing

TESTING_STATE = files_json[-1]

# Depickle

def get_pickle(path_to_file):
    with open(path_to_file, 'r') as f:
        return jsonpickle.decode(f.read())

data = get_pickle(f"{JSON_STATES_FOLDER}/{TESTING_STATE}")
print(len(data.finished_tagged_queue))