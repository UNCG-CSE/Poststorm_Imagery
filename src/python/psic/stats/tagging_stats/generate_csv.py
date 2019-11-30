# Imports.

import pandas as pd
import jsonpickle
import numpy as np
import matplotlib.pyplot as plt
import os, os.path
import dateutil.parser
from datetime import datetime
import statistics
# import argparse

# Global Constants.

SELF_PATH = os.getcwd()
DEFAULT_PATH_TO_JSON = os.path.join(SELF_PATH,'../tag_states.json')
DEFAULT_PATH_TO_OUTPUT_CSV = os.path.join(SELF_PATH,'../tagging_data.csv')


# Command line args. IM NOT GONNA USE TILL I LEARN MORE ABOUT IT, F

# parser = argparse.ArgumentParser(description='take JSON pickle and turn into CSV')

# parser.add_argument('--path', '-p', default=DEFAULT_PATH_TO_JSON,
#                     help='The path to the JSON pickle file to turn into a CSV')

# parser.add_argument('--out', '-o', default=DEFAULT_PATH_TO_OUTPUT_CSV,
#                     help='The path to place the CSV')

# Get args.
#args = parser.parse_args()

# Depickle tag state json.
depickled = None
with open(DEFAULT_PATH_TO_JSON, 'r') as f:
    depickled = jsonpickle.decode(f.read())

# Get the total number of images that are done being tagged,and number of images
# that are partially tagged.
total_finished =len(depickled.finished_tagged_queue)
total_incomplete_tagged=0
    
for image in depickled.pending_images_queue:
    if len(image.get_taggers()) > 0:
        total_incomplete_tagged+=1

total_skipped = len(depickled.max_skipped_queue)
total_currently_getting_tagged = len(depickled.current_image)

# How many images have circulated.
total_images_handled = total_incomplete_tagged + total_finished + total_skipped + total_currently_getting_tagged
tagged_ratio = total_incomplete_tagged/total_images_handled

df_basic_tag_data = pd.DataFrame([{ 
        'partial':total_incomplete_tagged,
        'done':total_finished,
        'skipped':total_skipped,
        'current':total_currently_getting_tagged,
        'tagged_ratio': tagged_ratio
    }])

print('\n==== Basic tagging data ====')
print(df_basic_tag_data.head())
print('\n')

# Now using the completly tagged image, gen the csv.

finished_images = depickled.finished_tagged_queue

df_of_image_tags = pd.DataFrame(dtype = int)

for image in finished_images:

    # This is the row we will populate and insert into the DF.
    image_dict_to_insert ={
        'image_id':image.get_rel_path().split("/")[-1],
        'list_of_taggers':list(image.get_taggers())
    }

    # First put in the tag data.
    image_dict_to_insert.update(image.final_tags )
    
    # List of times,from which we will sort to get min,max,mean,median and what not.
    starting_times = []
    ending_times = []
    assinged_times =[]
    session_times =[]

    # get the times and append to its respective list.
    for tagger in image.stats_tagging_start:
        starting_times.append(image.stats_tagging_start[tagger])
    
    for tagger in image.stats_tagging_stop:
        ending_times.append(image.stats_tagging_stop[tagger])
    
    for tagger in image.stats_tag_elapsed_assigned:
        assinged_times.append(image.stats_tag_elapsed_assigned[tagger])
    
    for tagger in image.stats_tag_elapsed_session:
        session_times.append(image.stats_tag_elapsed_session[tagger])

    # Put the time data in.
    image_dict_to_insert.update({
        'time_start':min(starting_times),
        'time_end':max(ending_times),
        'time_assigned':min(assinged_times),
        'time_elapsed':max(ending_times)-min(starting_times),
        'session_avg_time':statistics.mean(session_times),
        'session_max_time':max(session_times),
        'session_min_time':min(session_times),
        'session_median':statistics.median(session_times),
        'session_stdev':statistics.stdev(session_times)
    })

    # Convert our row dict into a df.
    tag_row_df = pd.DataFrame([image_dict_to_insert],dtype = int) 

    # Then insert.
    df_of_image_tags = pd.concat([df_of_image_tags,tag_row_df],sort=True, ignore_index = True)

# Now we have to clean the DF up.

# make all True/False into 1/0. 
df_of_image_tags.replace([False,True],[0,1], inplace=True)

columns_to_fill_na_wih_zero = [
        'washover',
        'impact',
        'development',
        'ocean',
        'terrain_inland','terrain_marsh','terrain_river','terrain_sandy_coastline','terrain_undefined'
    ]
# For these columns, replace NaN with 0's
df_of_image_tags[columns_to_fill_na_wih_zero] = df_of_image_tags[columns_to_fill_na_wih_zero].fillna(0.0).astype(int)

print('\n==== Head of DF to become CSV ====')
print(df_of_image_tags.head())
print('\n')

# Now generate CSV

df_of_image_tags.to_csv(DEFAULT_PATH_TO_OUTPUT_CSV)
print('done')