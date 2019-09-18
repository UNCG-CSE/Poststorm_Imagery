# Collector Script

**Document Updated:** {{ git_revision_date }}

In order to pull data from the NOAA website, [`collect.py`](../src/python/Poststorm_Imagery/collector/collect.py) 
is provided to automate the process of gathering data. Currently, the script can be called via command-line using 
specific arguments.

## Command-Line Quick Reference

|            Parameter | Argument(s) | Function                                            | Default Value          |
| -------------------: | ----------- | --------------------------------------------------- | ---------------------- |
|     `--storm`, `-s`  | *\<regex>*  | Search all storms for a specific term or pattern    | `.*`                   |
|       `--tar`, `-t`  | *\<regex>*  | Search all tar files for a specific term or pattern | `.*`                   |
|      `--path`, `-p`  | *\<path>*   | The path on your computer to save the files to      | `/data/tar_cache` |
|  `--no_status`, `-n` |             | Do not print out a report of all files found        | *False*                |
|  `--download`, `-d`  |             | Download the .tar files as well after listing them  | *False*                |
| `--overwrite`, `-o`  |             | Overwrite existing .tar files with the same name    | *False*                |


## Example Usage

-   To list all .tar files for *Hurricane Dorian*,
    `collect.py -s Dorian`
    will output something like
    ![Screenshot of `-s Dorian`](./collector_images/1.png)  
    
    
-   To list all .tar files for *Hurricane Dorian* that contain **jpg** in the file name,  
    `collect.py -s Dorian -t jpg`
    will output something like
    ![Screenshot of `-s Dorian -t jpg`](./collector_images/2.png)  
    
    
-   If you want a list of all .tar files that occurred in 2019 that contain **jpg** in the file name,  
    `collect.py  -t "2019[\w].*jpg"`
    will output something like
    ![Screenshot of `-s Dorian|Barry -t jpg`](./collector_images/3.png)  
    
    
-   Both the `--storm` and `--tar` flag also support regular expressions like  
    `collect.py -t jpg.*\D20\d{2}10\d{2}|(\D|^)20\d{2}10\d{2}.*jpg`
    which outputs all *jpg* files for *all storms* where the pictures were taken in *October* (month 10):
    ![Screenshot of `-t jpg.*\D20\d{2}10\d{2}|(\D|^)20\d{2}10\d{2}.*jpg`](./collector_images/4.png)  
    
    
-   Once you've found the results you want, simply add the download parameter, `-d`, before or after any parameter
    (*but not between a parameter and argument(s)*) to the statement like so:  
    `-t jpg.*\D20\d{2}10\d{2}|(\D|^)20\d{2}10\d{2}.*jpg` becomes `-t jpg.*\D20\d{2}10\d{2}|(\D|^)20\d{2}10\d{2}.*jpg -d`
    
    You should see an output like this below the file report, in the console:
    ![Screenshot of `-t jpg.*\D20\d{2}10\d{2}|(\D|^)20\d{2}10\d{2}.*jpg -d`](./collector_images/5.png)  
    
    
## Important Notes

The script will automatically download all .tar files listed, sequentially, to the [`--path`](#example-usage)
specified, or to the default cache folder if [`--path`](#example-usage) is left out of the parameters. 
Members of the C-Sick team, would run the command with `-p "D:\Shared drives\C-Sick\data"` 
if your *Google Drive File Stream* is your `D:` drive (*Windows*).
    
If the command doesn't understand one of your parameters, try 
again, but with quotes around any argument. Command-line treats anything separated by a space as two separate 
arguments, so something like `-s Hurricane Florence` should instead be `-s "Hurricane Florence"`
