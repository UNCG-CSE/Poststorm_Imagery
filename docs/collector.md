# Collector Script

In order to pull data from the NOAA website, [`collect.py`](../src/python/Poststorm_Imagery/collector/collect.py) 
is provided to automate the process of gathering data. Currently, the script can be called via command-line using 
specific arguments.

## Command-line Quick Reference

|           Parameter | Argument(s) | Function                                            | Default Value          |
| ------------------: | ----------- | --------------------------------------------------- | ---------------------- |
|     `--storm`, `-s` | *\<regex>*  | Search all storms for a specific term or pattern    | `.*`                   |
|       `--tar`, `-t` | *\<regex>*  | Search all tar files for a specific term or pattern | `.*`                   |
|      `--path`, `-p` | *\<path>*   | The path on your computer to save the files to      | `../../data/tar_cache` |
|  `--download`, `-d` |             | Download the .tar files as well after listing them  | *False* |
| `--overwrite`, `-o` |             | Overwrite existing .tar files with the same name    | *False* |


## Example Usage

-   To list all .tar files for *Hurricane Florence*,
    `collect.py -s Florence`
    will output something like
    
    ```  
    1.  Hurricane Florence (2018)  
        - (September 15 A 2018) 20180915a_RGB.tar [TIF]
        - (September 16 A 2018) 20180916a_RGB.tar [TIF]
        - (September 16 B 2018) 20180916b_RGB.tar [TIF]
        - (September 17 A 2018) 20180917a_RGB.tar [TIF]
        - (September 18 A 2018) 20180918a_RGB.tar [TIF]
        - (September 19 A 2018) 20180919a_RGB.tar [TIF]
        - (September 19 B 2018) 20180919b_RGB.tar [TIF]
        - (September 19 C 2018) 20180919c_RGB.tar [TIF]
        - (September 20 A 2018) 20180920a_RGB.tar [TIF]
        - (September 20 B 2018) 20180920b_RGB.tar [TIF]
        - (September 20 C 2018) 20180920c_RGB.tar [TIF]
        - (September 21 A 2018) 20180921a_RGB.tar [TIF]
        - (September 21 B 2018) 20180921b_RGB.tar [TIF]
        - (September 22 A 2018) 20180922a_RGB.tar [TIF]
        - (September 22 B 2018) 20180922b_RGB.tar [TIF]

    ```
    
-   To list all .tar files for *Hurricane Florence* that were taken on **September 20th**,  
    `collect.py -s Florence -t "Sep.* 20 "`
    will output something like
    
    ```  
    1.  Hurricane Florence (2018)
        - (September 20 A 2018) 20180920a_RGB.tar [TIF]
        - (September 20 B 2018) 20180920b_RGB.tar [TIF]
        - (September 20 C 2018) 20180920c_RGB.tar [TIF]
    ```
    
-   If you want a list of all .tar files for *Hurricane Florence* & *Hurricane Barry*,  
    `collect.py -s Florence|Barry`
    will output something like
    
    ```  
    1.  Hurricane Barry (2019)
        - (July 16 2019) 20190716a_RGB.tar [TIF]
        - (July 17 2019) 20190717a_RGB.tar [TIF]
        - (July 19 2019) 20190719a_RGB.tar [TIF]

    2.  Hurricane Florence (2018)
        - (September 15 A 2018) 20180915a_RGB.tar [TIF]
        - (September 16 A 2018) 20180916a_RGB.tar [TIF]
        - (September 16 B 2018) 20180916b_RGB.tar [TIF]
        - (September 17 A 2018) 20180917a_RGB.tar [TIF]
        - (September 18 A 2018) 20180918a_RGB.tar [TIF]
        - (September 19 A 2018) 20180919a_RGB.tar [TIF]
        - (September 19 B 2018) 20180919b_RGB.tar [TIF]
        - (September 19 C 2018) 20180919c_RGB.tar [TIF]
        - (September 20 A 2018) 20180920a_RGB.tar [TIF]
        - (September 20 B 2018) 20180920b_RGB.tar [TIF]
        - (September 20 C 2018) 20180920c_RGB.tar [TIF]
        - (September 21 A 2018) 20180921a_RGB.tar [TIF]
        - (September 21 B 2018) 20180921b_RGB.tar [TIF]
        - (September 22 A 2018) 20180922a_RGB.tar [TIF]
        - (September 22 B 2018) 20180922b_RGB.tar [TIF]
    ```
    
-   If you want a list of all .tar files for storms from 2018**,  
    `collect.py -s 2018`
    will output something like
    
    ```  
    1.  Hurricane Michael (2018)
        - (October 11 A 2018) 20181011a_RGB.tar [TIF]
        - (October 12 A 2018) 20181012a_RGB.tar [TIF]
        - (October 12 B 2018) 20181012b_RGB.tar [TIF]
        - (October 13 A 2018) 20181013a_RGB.tar [TIF]
        - (October 14 A 2018) 20181014a_RGB.tar [TIF]

    2.  Hurricane Florence (2018)
        - (September 15 A 2018) 20180915a_RGB.tar [TIF]
        - (September 16 A 2018) 20180916a_RGB.tar [TIF]
        - (September 16 B 2018) 20180916b_RGB.tar [TIF]
        - (September 17 A 2018) 20180917a_RGB.tar [TIF]
        - (September 18 A 2018) 20180918a_RGB.tar [TIF]
        - (September 19 A 2018) 20180919a_RGB.tar [TIF]
        - (September 19 B 2018) 20180919b_RGB.tar [TIF]
        - (September 19 C 2018) 20180919c_RGB.tar [TIF]
        - (September 20 A 2018) 20180920a_RGB.tar [TIF]
        - (September 20 B 2018) 20180920b_RGB.tar [TIF]
        - (September 20 C 2018) 20180920c_RGB.tar [TIF]
        - (September 21 A 2018) 20180921a_RGB.tar [TIF]
        - (September 21 B 2018) 20180921b_RGB.tar [TIF]
        - (September 22 A 2018) 20180922a_RGB.tar [TIF]
        - (September 22 B 2018) 20180922b_RGB.tar [TIF]

    3.  Tropical Storm Gordon (2018)
        - (September 06 2018 ) 20180906a_RGB.tar [TIF]
        - (September 06 2018 ) 20180906a_jpgs.tar [RAW JPEG]
        - (September 07 2018 ) 20180907a_RGB.tar [TIF]
        - (September 07 2018 ) 20180907a_jpgs.tar [RAW JPEG]
    ```
    
-   Once you've found the results you want, simply add the download parameter, `-d`, before or after any parameter
    (*but not between a parameter and argument(s)*) to the statement like so:  
    `collect.py -s Florence -t "Sep.* 20 "` becomes `collect.py -s Florence -t "Sep.* 20 " -d`
    
    You should see an output like this in the console:
    ```
    1.  Hurricane Florence (2018)
        - (September 20 A 2018) 20180920a_RGB.tar [TIF]
        - (September 20 B 2018) 20180920b_RGB.tar [TIF]
        - (September 20 C 2018) 20180920c_RGB.tar [TIF]
    
    Downloading files...
    Downloading 20180920a_RGB.tar:   0%|          | 1/17107 [00:03<17:36:58,  3.71s/MiB]
    ```
    
    The script will automatically download all .tar files listed, sequentially, to the [`--path`](#example-usage)
    specified, or to the default cache folder. For members of the C-Sick team, you would run the command with 
    `-p "D:\Shared drives\C-Sick\data"` if your *Google Drive File Stream* is your `D:` drive (*Windows*).
    
    The parameters `-p "D:\Shared drives\C-Sick\data" -s Florence -t "Sep.* 20 " -d` would download all files for 
    *Hurricane Florence* taken on September 20th and save them to the shared drive. All parameters are optional and 
    default to the values listed [above](#example-usage). If the command doesn't understand one of your parameters, try 
    again, but with quotes around any argument with spaces in the argument.
