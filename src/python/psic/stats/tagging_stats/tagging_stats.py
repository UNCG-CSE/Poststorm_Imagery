#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import jsonpickle
import numpy as np
import matplotlib.pyplot as plt
import os, os.path
import dateutil.parser


# In[2]:


FILE_AS_ROOT = True
SELF_PATH = os.path.dirname(os.path.abspath(__file__))
FILE_TO_ROOT = '../../../../../../' if not FILE_AS_ROOT else '../'
PATH_TO_JSON_STATES = f"{FILE_TO_ROOT}tagging_json_states"

print('aaaa',SELF_PATH)


# In[3]:


TOTAL_JSON_STATES = (len([name for name in os.listdir(PATH_TO_JSON_STATES) if os.path.isfile(os.path.join(PATH_TO_JSON_STATES, name))]))
print(TOTAL_JSON_STATES)


# In[ ]:


def get_pickle(path_to_file):
    with open(path_to_file, 'r') as f:
        return jsonpickle.decode(f.read())


# In[ ]:


def how_many_tagged(pickle_file):
    
    done_tagging_count=len(pickle_file.finished_tagged_queue)
    tagged_but_not_done_count=0
    
    for image in pickle_file.pending_images_queue:
        if len(image.get_taggers()) > 0:
            tagged_but_not_done_count-=-1
    
    return pd.DataFrame([{ 
        'not_done':tagged_but_not_done_count,
        'done':done_tagging_count,
        'tagged_ratio': tagged_but_not_done_count/(tagged_but_not_done_count+done_tagging_count)
     }])


# In[ ]:


def get_all_json_states(path_states):
    files = os.listdir(path_states)
    filter_by_type = [f for f in files if f[-4:] == 'json']
    filter_by_type.sort()
    return filter_by_type


# In[4]:


files_json = get_all_json_states(PATH_TO_JSON_STATES)
print(files_json[1:4])


# In[ ]:


def get_tagged_ratio(files):
    
    main_df = pd.DataFrame()
    
    for file in files[::50]:
        path = f"{PATH_TO_JSON_STATES}/{file}"
        
        remove_name = file.split('assigner_state-root-')[-1]
        date_string = remove_name.split('.json')[0]
        removed_nano = date_string.split('.')[0].replace("_",":")
        time = dateutil.parser.parse(removed_nano).strftime('%s')
        time_df= pd.DataFrame([{'time':time,'name':date_string}])    
        
        tag_df = how_many_tagged(get_pickle(path))
        
        combined_df = pd.concat([time_df,tag_df],axis=1, sort=False)
        main_df = pd.concat([combined_df,main_df],ignore_index=True)
        
    return main_df


# In[ ]:


df = get_tagged_ratio(files_json)
df_time_sort = df.sort_values(by=['time'])


# In[ ]:


df_time_sort.head()


# In[ ]:


pd.Series(df_time_sort['tagged_ratio'].values).plot.line()


# In[ ]:




