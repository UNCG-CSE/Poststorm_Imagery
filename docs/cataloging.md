# Cataloging Script

**Document Updated:** {{ git_revision_date }}

Once data is downloaded and unpacked, the data can be cataloged in order to more quickly access key information such as 
GPS data for each image, file size, and date taken to help with statistical and spacial analysis. 
	

## Command-Line Quick Reference

|            Parameter | Argument(s)    | Function                                                                                     | Default Value            |
| -------------------: | -------------- | -------------------------------------------------------------------------------------------- | ------------------------ |
|       `--path`, `-p` | *<path\>*      | The path on your computer to start looking for files and save the catalog to                 | `#!text /data/tar_cache` |
|  `--extension`, `-e` | *<extension\>* | Only add files with this extension to the catalog                                            | `jpg`                    |
|     `--fields`, `-e` | *<Set\>* [^1]  | Only include these fields from the .geom and system values                                   | *(See Note) [^1]*        |
|      `--debug`, `-d` |                | Include parameter to output debug information to console                                     | *False*                  |
|  `--verbosity`, `-v` | *<level\>*     | The amount of information to log to console (0 = only errors, 1 = low, 2 = medium, 3 = high) | `#!text 1`               |

[^1]:   !!! note "Modifying Catalog Contents"  
            Any field within the `.geom` file of all images can be added to the catalog by simply changing the `--fields` flag. 
            The default fields are `{'file', 'size', 'date', 'll_lat', 'll_lon', 'lr_lat', 'lr_lon', 'ul_lat', 'ul_lon', 'ur_lat', 
            'ur_lon'}` where `file` is parsed from the unpacked archive's folder name (`#!text .../20180919a_jpgs/...` 
            --> `#!text 2018/09/19`) and `#!text size` is determined by Python's `os.path.getsize()` function.
        
    
    
!!! warning
    If the command doesn't understand one of your parameters, try 
    again, but with quotes around any argument. Command-line treats anything separated by a space as two separate 
    arguments, so something like `-p C:\some dir\data\tar_cache\Florence` should instead be 
    `-p "C:\some dir\data\tar_cache\Florence"`