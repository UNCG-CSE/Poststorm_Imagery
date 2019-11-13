import pandas as pd
import jsonpickle
import numpy as np

JSON_FILE_TO_IMPORT = "../../../../../../tagging_data_personal.json"  # "test.json"

with open(JSON_FILE_TO_IMPORT, 'r') as f:
    data = jsonpickle.decode(f.read())

    done_tagging_count=len(data.finished_tagged_queue)

    tagged_but_not_done_count=0
    for image in data.pending_images_queue:
        if len(image.get_taggers()) > 0:
            tagged_but_not_done_count-=-1
    
    print(f"{tagged_but_not_done_count} images have been tagged, but not completely")
    print(f"{done_tagging_count} images have been tagged completely")
    print(f"{tagged_but_not_done_count+done_tagging_count} images have been tagged, completely or not")
