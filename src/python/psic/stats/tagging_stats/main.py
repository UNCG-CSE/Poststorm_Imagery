import pandas as pd
import jsonpickle
import numpy as np

JSON_FILE_TO_IMPORT = "../tagging_data_personal.json"  # "test.json"


def get_pickle(path_to_file):
    with open(JSON_FILE_TO_IMPORT, 'r') as f:
        return jsonpickle.decode(f.read())
        
def how_many_taggged(pickle_file):
    done_tagging_count=len(pickle_file.finished_tagged_queue)

    tagged_but_not_done_count=0
    for image in pickle_file.pending_images_queue:
        if len(image.get_taggers()) > 0:
            tagged_but_not_done_count-=-1

    print(f"{tagged_but_not_done_count} images have been tagged, but not completely")
    print(f"{done_tagging_count} images have been tagged completely")
    print(f"{tagged_but_not_done_count+done_tagging_count} images have been tagged, completely or not")

data = get_pickle(JSON_FILE_TO_IMPORT)

print(data.pending_images_queue[-1].taggers)

