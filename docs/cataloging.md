# Cataloging Script

**Document Updated:** {{ git_revision_date }}

Once data is downloaded and unpacked, the data can be cataloged (`pstorm catalog <args>`) in order to more quickly
access key information such as GPS data for each image, file size, and date taken to help with statistical and
spacial analysis.


## Command-Line Quick Reference

|            Parameter | Argument(s)    | Function                                                                                     | Default Value       |
| -------------------: | -------------- | -------------------------------------------------------------------------------------------- | ------------------- |
|  `--extension`, `-e` | *<extension\>* | Only add files with this extension to the catalog                                            | `jpg`               |
|     `--fields`, `-e` | *<Set\>*       | Only include these fields from the .geom and system values                                   | *(See Note)*        |
|      `--debug`, `-d` |                | Include parameter to output debug information to console                                     | *False*             |
|  `--verbosity`, `-v` | *<level\>*     | The amount of information to log to console (0 = only errors, 1 = low, 2 = medium, 3 = high) | `1`                 |

!!! note "Modifying Catalog Contents"
            Any field within the `.geom` file of all images can be added to the catalog by simply changing the `--fields` flag.
            The default fields are `{'file', 'storm_id', 'archive', 'image', 'date', 'size', 'geom_checksum', 'll_lat',
            'll_lon', 'lr_lat', 'lr_lon', 'ul_lat', 'ul_lon', 'ur_lat', 'ur_lon'}`.

!!! warning
    If the command doesn't understand one of your parameters, try
    again, but with quotes around any argument. Command-line treats anything separated by a space as two separate
    arguments, so something like

    ```
    -e {'file', 'storm_id', 'archive', 'image', 'date', 'size', 'geom_checksum', 'll_lat',
    'll_lon', 'lr_lat', 'lr_lon', 'ul_lat', 'ul_lon', 'ur_lat', 'ur_lon'}
    ```

    should instead be

    ```
    -e "{'file', 'storm_id', 'archive', 'image', 'date', 'size', 'geom_checksum', 'll_lat', 'll_lon', 'lr_lat',
    'lr_lon', 'ul_lat', 'ul_lon', 'ur_lat', 'ur_lon'}"
    ```


??? quote "Catalog Snippet Example (Florence.csv)"
    ```
        file                                storm_id    archive         image           size        date        ur_lat              lr_lon              ur_lon              ll_lat              ul_lon              ll_lon              lr_lat              geom_checksum                       ul_lat
    0   20180919b_jpgs/jpgs/P26276665.jpg   florence    20180919b_jpgs  P26276665.jpg   5921685     2018/09/19  34.191330528689896  -77.8172986188853   -77.8071351918187   34.2084190030626    -77.7966678384306   -77.8109531705992   34.2002698812517    22bfdc9e8c7dd77694051c42b73ef383    34.2044620318067
    1   20180919b_jpgs/jpgs/P26275221.jpg   florence    20180919b_jpgs  P26275221.jpg   7856304     2018/09/19  34.7371165394654    -76.77522871514509  -76.7749606421931   34.7477255105265    -76.7604501831659   -76.7643344559212   34.745983715257395  2bf6434e14c78918a083b45d8e8c84e3    34.739330560690604
    2   20180919b_jpgs/jpgs/C26276792.jpg   florence    20180919b_jpgs  C26276792.jpg   7416479     2018/09/19  34.1162796503269    -77.87568430993849  -77.8792119685572   34.1210497955716    -77.8652190981454   -77.86175166742471  34.1254405298099    4028837f1fd5c4d272b3fcbf086da858    34.112801566182604
    3   20180919b_jpgs/jpgs/P26272498.jpg   florence    20180919b_jpgs  P26272498.jpg   7077670     2018/09/19  35.193880664552495  -77.1145840941805   -77.12685826117591  35.1924425087302    -77.1143746980758   -77.1067252477598   35.1994469823763    6936f486b508e47daa4170f59ec40493    35.1834462909063
    4   20180919b_jpgs/jpgs/S26272099.jpg   florence    20180919b_jpgs  S26272099.jpg   7181557     2018/09/19  35.2185091526623    -77.2066561006074   -77.2176882132229   35.220158733872     -77.20315073385841  -77.1973995512931   35.2259529314223    7cf0657aa2514cb44a9b3a911dfd6327    35.2089104765192
    ```
