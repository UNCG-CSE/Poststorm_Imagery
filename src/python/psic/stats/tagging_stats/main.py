import pandas as pd
import jsonpickle
import numpy as np

FILE_AS_ROOT = False

JSON_FILE_TO_IMPORT = f"{'../../../../../../' if FILE_AS_ROOT else '../'}tagging_data_personal.json" 
SCRIPT_PATH = "./src/python/psic/stats/tagging_stats"
FILE_TO_TAG_RATIO = f"{'./' if FILE_AS_ROOT else './src/python/psic/stats/tagging_stats'}tag_ratio.csv"

# Used to get a pickgle at a specified path.
def get_pickle(path_to_file):
    with open(JSON_FILE_TO_IMPORT, 'r') as f:
        return jsonpickle.decode(f.read())
        
# Function to display some information about the json pickle file.
def how_many_taggged(pickle_file):
    done_tagging_count=len(pickle_file.finished_tagged_queue)

    tagged_but_not_done_count=0
    for image in pickle_file.pending_images_queue:
        if len(image.get_taggers()) > 0:
            tagged_but_not_done_count-=-1

    print(f"{tagged_but_not_done_count} images have been tagged, but not completely")
    print(f"{done_tagging_count} images have been tagged completely")
    print(f"{tagged_but_not_done_count+done_tagging_count} images have been tagged, completely or not")

# Get the json pickle
data = get_pickle(JSON_FILE_TO_IMPORT)

tag_ratio_data = pd.read_csv(FILE_TO_TAG_RATIO)
print(tag_ratio_data.head())