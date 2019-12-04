# Collector Script

**Document Updated:** {{ git_revision_date }}

In order to pull data from the NOAA website, `collect.py` (`pstorm collect <args>`) is provided to automate the
process of gathering data. The script can be called via command-line using the arguments below.

!!! warning "Collector Caveat"

    The script cannot retrieve archives for the following storms because they are not publicly available in archive
    form:

    20.  	North Dakota Flooding (2011)
    31.  	Hurricane Dennis (2005)
    32.  	Hurricane Ivan (2004)
    33.  	Hurricane Jeanne (2004)
    34.  	Hurricane Isabel (2003)


## Command-Line Quick Reference

|            Parameter | Argument(s) | Function                                                | Default Value                           |
| -------------------: | ----------- | ------------------------------------------------------- | --------------------------------------- |
|     `--storm`, `-s`  | *<regex\>*  | Search all storms for a specific term or pattern        | `.*`                                    |
|   `--archive`, `-a`  | *<regex\>*  | Search all archive files for a specific term or pattern | `.*`                                    |
|      `--path`, `-p`  | *<path\>*   | The path on your computer to save the files to          | `<user_home>/psi/collect/data/archives` |
| `--no_status`, `-n`  |             | Do not print out a report of all files found            | *False*                                 |
|  `--download`, `-d`  |             | Download the archive files as well after listing them   | *False*                                 |
| `--overwrite`, `-o`  |             | Overwrite existing archive files with the same name     | *False*                                 |



!!! warning
    If the command doesn't understand one of your parameters, try
    again, but with quotes around any argument. Command-line treats anything separated by a space as two separate
    arguments, so something like `-s Hurricane Florence` should instead be `-s "Hurricane Florence"`


!!! note "Important Note"

    The script will automatically download all archive files listed, sequentially, to the `--path` specified, or to the
    default cache folder if `--path` is left out of the parameters. Members of the P-Sick team would run the command
    with `-p "G:\Shared drives\P-Sick\data"` assuming they have *Google Drive File Stream* as their `G:`
    drive (*Windows*).


## Example Usages

1.  To list all archive files for *Hurricane Dorian*,
    `pstorm collect -s Dorian`

    ??? quote "Resulting Output"
        ```text
        Download Status Report (September 23, 2019 at 02:20 PM) <-s Dorian -t .* -p [...]>

        1.  	Hurricane Dorian (2019)
                - 20190904a_RGB.tar  ... 525.74 MiBs  ... Not downloaded.
                - 20190904a_jpgs.tar  ... 1.73 GiBs  ... Not downloaded.
                - 20190905a_RGB.tar  ... 18.32 GiBs  ... Not downloaded.
                - 20190905a_jpgs.tar  ... 18.12 GiBs  ... Not downloaded.
                - 20190905b_RGB.tar  ... 9.9 GiBs  ... Not downloaded.
                - 20190905b_jpgs.tar  ... 4.64 GiBs  ... Not downloaded.
                - 20190906a_RGB.tar  ... 8.4 GiBs  ... Not downloaded.
                - 20190906a_jpgs.tar  ... 9.14 GiBs  ... Not downloaded.
                - 20190906b_RGB.tar  ... 15.97 GiBs  ... Not downloaded.
                - 20190906b_jpgs.tar  ... 16.89 GiBs  ... Not downloaded.
                - 20190907a_RGB.tar  ... 7.86 GiBs  ... Not downloaded.
                - 20190907a_jpgs.tar  ... 7.79 GiBs  ... Not downloaded.
                - 20190907b_RGB.tar  ... 7.63 GiBs  ... Not downloaded.
                - 20190907b_jpgs.tar  ... 6.55 GiBs  ... Not downloaded.
                - 20190917a_RGB.tar  ... 11.88 GiBs  ... Not downloaded.
                - 20190917a_jpgs.tar  ... 21.31 GiBs  ... Not downloaded.
                - 20190917b_RGB.tar  ... 11.26 GiBs  ... Not downloaded.
                - 20190917b_jpgs.tar  ... 19.95 GiBs  ... Not downloaded.
                - 20190918a_RGB.tar  ... 5.68 GiBs  ... Not downloaded.
                - 20190918b_RGB.tar  ... 4.59 GiBs  ... Not downloaded.
                - 20190918b_jpgs.tar  ... 8.42 GiBs  ... Not downloaded.
                - 20190919a_RGB.tar  ... 12.27 GiBs  ... Not downloaded.
                - 20190919a_jpgs.tar  ... 15.26 GiBs  ... Not downloaded.
                - 20190920a_RGB.tar  ... 4.49 GiBs  ... Not downloaded.
                - 20190920a_jpgs.tar  ... 5.1 GiBs  ... Not downloaded.
                Total: 0.0 KiBs / 253.66 GiBs  (0%)

        Total: 0.0 KiBs / 253.66 GiBs  (0%)
        ```

2.  To list all archive files for *Hurricane Dorian* that contain **jpg** in the file name,
    `pstorm collect -s Dorian -a jpg`

    ??? quote "Resulting Output"
        ```text
        Download Status Report (September 23, 2019 at 02:28 PM) <-s Dorian -a jpg -p [...]>

        1.  	Hurricane Dorian (2019)
                - 20190904a_jpgs.tar  ... 1.73 GiBs  ... Not downloaded.
                - 20190905a_jpgs.tar  ... 18.12 GiBs  ... Not downloaded.
                - 20190905b_jpgs.tar  ... 4.64 GiBs  ... Not downloaded.
                - 20190906a_jpgs.tar  ... 9.14 GiBs  ... Not downloaded.
                - 20190906b_jpgs.tar  ... 16.89 GiBs  ... Not downloaded.
                - 20190907a_jpgs.tar  ... 7.79 GiBs  ... Not downloaded.
                - 20190907b_jpgs.tar  ... 6.55 GiBs  ... Not downloaded.
                - 20190917a_jpgs.tar  ... 21.31 GiBs  ... Not downloaded.
                - 20190917b_jpgs.tar  ... 19.95 GiBs  ... Not downloaded.
                - 20190918b_jpgs.tar  ... 8.42 GiBs  ... Not downloaded.
                - 20190919a_jpgs.tar  ... 15.26 GiBs  ... Not downloaded.
                - 20190920a_jpgs.tar  ... 5.1 GiBs  ... Not downloaded.
                Total: 0.0 KiBs / 134.9 GiBs  (0%)

        Total: 0.0 KiBs / 134.9 GiBs  (0%)
        ```


-   If you want a list of all archive files that occurred in 2019 that contain **jpg** in the file name,
    `pstorm collect -s 2019 -a jpg`

    ??? quote "Resulting Output"
        ```text
        Download Status Report (September 23, 2019 at 02:37 PM) <-s 2019 -a jpg -p [...]>

        1.  	Hurricane Dorian (2019)
                - 20190904a_jpgs.tar  ... 1.73 GiBs  ... Not downloaded.
                - 20190905a_jpgs.tar  ... 18.12 GiBs  ... Not downloaded.
                - 20190905b_jpgs.tar  ... 4.64 GiBs  ... Not downloaded.
                - 20190906a_jpgs.tar  ... 9.14 GiBs  ... Not downloaded.
                - 20190906b_jpgs.tar  ... 16.89 GiBs  ... Not downloaded.
                - 20190907a_jpgs.tar  ... 7.79 GiBs  ... Not downloaded.
                - 20190907b_jpgs.tar  ... 6.55 GiBs  ... Not downloaded.
                - 20190917a_jpgs.tar  ... 21.31 GiBs  ... Not downloaded.
                - 20190917b_jpgs.tar  ... 19.95 GiBs  ... Not downloaded.
                - 20190918b_jpgs.tar  ... 8.42 GiBs  ... Not downloaded.
                - 20190919a_jpgs.tar  ... 15.26 GiBs  ... Not downloaded.
                - 20190920a_jpgs.tar  ... 5.1 GiBs  ... Not downloaded.
                Total: 0.0 KiBs / 134.9 GiBs  (0%)

        2.  	Hurricane Barry (2019)
                - 20190716a_jpgs.tar  ... 40.19 GiBs  ... Not downloaded.
                - 20190717a_jpgs.tar  ... 11.19 GiBs  ... Not downloaded.
                - 20190719a_jpgs.tar  ... 4.66 GiBs  ... Not downloaded.
                Total: 0.0 KiBs / 56.04 GiBs  (0%)

        Total: 0.0 KiBs / 190.94 GiBs  (0%)
        ```


-   Both the `--storm` and `--archive` flags also support regular expressions like
    `pstorm collect -a jpg.*\D20\d{2}10\d{2}|(\D|^)20\d{2}10\d{2}.*jpg`
    which outputs all *jpg* files for *all storms* where the pictures were taken in *October* (month 10) of any year:

    ??? quote "Resulting Output"
        ```text
        Download Status Report (September 23, 2019 at 02:38 PM) <-s .* -a jpg.*\D20\d{2}10\d{2}|(\D|^)20\d{2}10\d{2}.*jpg -p [...]>

        1.  	Hurricane Dorian (2019)
                <No archive files detected in index.html>

        2.  	Hurricane Barry (2019)
                <No archive files detected in index.html>

        3.  	Hurricane Michael (2018)
                - 20181011a_jpgs.tar  ... 22.56 GiBs  ... Not downloaded.
                - 20181012a_jpgs.tar  ... 15.65 GiBs  ... Not downloaded.
                - 20181012b_jpgs.tar  ... 12.86 GiBs  ... Not downloaded.
                - 20181013a_jpgs.tar  ... 16.15 GiBs  ... Not downloaded.
                - 20181014a_jpgs.tar  ... 23.24 GiBs  ... Not downloaded.
                Total: 0.0 KiBs / 90.45 GiBs  (0%)

        4.  	Hurricane Florence (2018)
                <No archive files detected in index.html>

        5.  	Tropical Storm Gordon (2018)
                <No archive files detected in index.html>

        6.  	Hurricane Nate (2017)
                <No archive files detected in index.html>

        7.  	Hurricane Maria (2017)
                <No archive files detected in index.html>

        8.  	Hurricane Irma (2017)
                <No archive files detected in index.html>

        9.  	Hurricane Harvey (2017)
                <No archive files detected in index.html>

        10.  	Hurricane Matthew (2016)
                <No archive files detected in index.html>

        11.  	Louisiana Flooding (2016)
                <No archive files detected in index.html>

        12.  	Midwest U.S. Flooding (2015)
                <No archive files detected in index.html>

        13.  	Illinois Tornadoes (2015)
                <No archive files detected in index.html>

        14.  	Hurricane Arthur (2014)
                <No archive files detected in index.html>

        15.  	Hurricane Sandy (2012)
                <No archive files detected in index.html>

        16.  	Hurricane Isaac (2012)
                <No archive files detected in index.html>

        17.  	Hurricane Irene (2011)
                <No archive files detected in index.html>

        18.  	Joplin, MO Tornado (2011)
                <No archive files detected in index.html>

        19.  	Tuscaloosa, AL Tornado (2011)
                <No archive files detected in index.html>

        20.  	North Dakota Flooding (2011)
                <No archive files detected in index.html>

        21.  	Hurricane Earl (2010)
                <No archive files detected in index.html>

        22.  	Nor'Easter Nov09 (2009)
                <No archive files detected in index.html>

        23.  	Hurricane Ike (2008)
                <No archive files detected in index.html>

        24.  	Hurricane Gustav (2008)
                <No archive files detected in index.html>

        25.  	Hurricane Humberto (2007)
                <No archive files detected in index.html>

        26.  	Tropical Storm Ernesto (2006)
                <No archive files detected in index.html>

        27.  	Hurricane Wilma (2005)
                <No archive files detected in index.html>

        28.  	Hurricane Rita (2005)
                <No archive files detected in index.html>

        29.  	Hurricane Ophelia (2005)
                <No archive files detected in index.html>

        30.  	Hurricane Katrina (2005)
                <No archive files detected in index.html>

        31.  	Hurricane Dennis (2005)
                <No archive files detected in index.html>

        32.  	Hurricane Ivan (2004)
                <No archive files detected in index.html>

        33.  	Hurricane Jeanne (2004)
                <No archive files detected in index.html>

        34.  	Hurricane Isabel (2003)
                <No archive files detected in index.html>

        Total: 0.0 KiBs / 90.45 GiBs  (0%)
        ```



-   Once you've found the results you want, simply add the download parameter, `-d`, before or after any parameter
    (*but not between a parameter and argument(s)*) to the statement like so:
    `-a jpg.*\D20\d{2}10\d{2}|(\D|^)20\d{2}10\d{2}.*jpg` becomes
    `-a jpg.*\D20\d{2}10\d{2}|(\D|^)20\d{2}10\d{2}.*jpg -d`

    You should see an output like this below the file report, in the console:

    ??? quote "Download Progress Bar"

        ```text
        Downloading files...
        Downloading 20181011a_jpgs.tar:   0%|          | 20/23097 [00:04<1:24:32,  4.55MiB/s]
        ```
