# Cataloging Script

**Document Updated:** {{ git_revision_date }}

Once data is downloaded and unpacked, the data can be cataloged in order to more quickly access key information such as
GPS data for each image, file size, and date taken to help with statistical and spacial analysis.


## Command-Line Quick Reference

|            Parameter | Argument(s)    | Function                                                                                     | Default Value            |
| -------------------: | -------------- | -------------------------------------------------------------------------------------------- | ------------------------ |
|       `--path`, `-p` | *<path\>*      | The path on your computer to start looking for files and save the catalog to                 | `/data/archive_cache` |
|  `--extension`, `-e` | *<extension\>* | Only add files with this extension to the catalog                                            | `jpg`                    |
|     `--fields`, `-e` | *<Set\>*       | Only include these fields from the .geom and system values                                   | *(See Note) [^1]*        |
|      `--debug`, `-d` |                | Include parameter to output debug information to console                                     | *False*                  |
|  `--verbosity`, `-v` | *<level\>*     | The amount of information to log to console (0 = only errors, 1 = low, 2 = medium, 3 = high) | `1`               |

!!! warning
    If the command doesn't understand one of your parameters, try
    again, but with quotes around any argument. Command-line treats anything separated by a space as two separate
    arguments, so something like `-p C:\some dir\data\archive_cache\Florence` should instead be
    `-p "C:\some dir\data\archive_cache\Florence"`


??? quote "Catalog Snippet Example (data/catalog.csv)"
    ```
        file	                                    size	date	    ur_lon	        ur_lat	    lr_lon	        ul_lon	        ll_lat	    ul_lat	    lr_lat	    ll_lon
    0	Florence/20180919c_jpgs/jpgs/C26256485.jpg	8265645	9/19/2018	-79.08661668	34.67886016	-79.07961335	-79.0901903	    34.66892408	34.67104059	34.67651003	-79.08320942
    1	Florence/20180919c_jpgs/jpgs/C26271559.jpg	9568353	9/19/2018	-79.28688193	34.77472521	-79.29379523	-79.28454167	34.78380964	34.78259516	34.77622451	-79.29171139
    2	Florence/20180919c_jpgs/jpgs/C26259098.jpg	9094248	9/19/2018	-79.057326	    34.64443293	-79.06458904	-79.05504498	34.65387737	34.65260206	34.64596058	-79.06239303
    3	Florence/20180919c_jpgs/jpgs/C26248841.jpg	7226118	9/19/2018	-78.9760616	    33.79260652	-78.98227988	-78.9812113	    33.7963527	33.79986971	33.78950101	-78.9876131
    4	Florence/20180919c_jpgs/jpgs/C26258084.jpg	8531607	9/19/2018	-79.08531498	34.6652912	-79.07834599	-79.08884077	34.65542896	34.65750533	34.66309127	-79.08176969
    5	Florence/20180919c_jpgs/jpgs/C26256710.jpg	9134932	9/19/2018	-79.27612125	34.71659796	-79.26909566	-79.27942806	34.70683734	34.70880362	34.71443632	-79.27246624
    6	Florence/20180919c_jpgs/jpgs/C26266876.jpg	9384940	9/19/2018	-79.09108099	34.62906236	-79.08382438	-79.09448621	34.61898235	34.62104284	34.62657757	-79.08765149
    7	Florence/20180919c_jpgs/jpgs/C26247907.jpg	8844693	9/19/2018	-78.96842531	33.8416665	-78.97487177	-78.9740459	    33.84523485	33.8487322	33.83835318	-78.980186
    8	Florence/20180919c_jpgs/jpgs/C26273756.jpg	8463839	9/19/2018	-79.33294776	34.75866461	-79.33981982	-79.32982997	34.76827153	34.76672858	34.76036655	-79.33745904
    9	Florence/20180919c_jpgs/jpgs/C26270728.jpg	8898730	9/19/2018	-79.09726724	34.58978362	-79.09016933	-79.10020402	34.58011418	34.58187603	34.58795537	-79.09302109
    10	Florence/20180919c_jpgs/jpgs/C26277188.jpg	8721410	9/19/2018	-79.29768201	34.71437422	-79.29060937	-79.30095442	34.70455202	34.70645011	34.7121787	-79.29389662
    11	Florence/20180919c_jpgs/jpgs/C26266313.jpg	8764332	9/19/2018	-79.03562243	34.61333059	-79.0430049	    -79.03314792	34.62298809	34.62155365	34.61511809	-79.04036266
    12	Florence/20180919c_jpgs/jpgs/C26273283.jpg	9148681	9/19/2018	-79.30310652	34.76668714	-79.296192	    -79.30614578	34.75717656	34.7589053	34.76470873	-79.29912521
    13	Florence/20180919c_jpgs/jpgs/C26259109.jpg	7879353	9/19/2018	-79.04782188	34.64243177	-79.05504009	-79.04523263	34.65200642	34.65056659	34.64412007	-79.05257609
    14	Florence/20180919c_jpgs/jpgs/C26256642.jpg	8786732	9/19/2018	-79.21778203	34.70516559	-79.21071458	-79.22099979	34.69540914	34.697334	34.70300387	-79.21406625
    15	Florence/20180919c_jpgs/jpgs/C26260465.jpg	8119057	9/19/2018	-79.17774989	34.65609152	-79.18494354	-79.17513935	34.66568373	34.66421355	34.6576701	-79.18259539
    16	Florence/20180919c_jpgs/jpgs/C26274326.jpg	8682969	9/19/2018	-79.35979201	34.76548726	-79.35282474	-79.36291047	34.75590343	34.7577536	34.76336594	-79.35607653
    17	Florence/20180919c_jpgs/jpgs/C26275349.jpg	8532846	9/19/2018	-79.33914349	34.74817595	-79.33220113	-79.3426105	    34.73837696	34.74037772	34.74594119	-79.33557598
    18	Florence/20180919c_jpgs/jpgs/C26267489.jpg	8835280	9/19/2018	-79.21406618	34.63576507	-79.22140613	-79.21156486	34.64538086	34.64390819	34.63764472	-79.21860893
    ```


[^1]:   !!! note "Modifying Catalog Contents"
            Any field within the `.geom` file of all images can be added to the catalog by simply changing the `--fields` flag.
            The default fields are `{'file', 'size', 'date', 'll_lat', 'll_lon', 'lr_lat', 'lr_lon', 'ul_lat', 'ul_lon', 'ur_lat',
            'ur_lon'}` where `file` is parsed from the unpacked archive's folder name (`.../20180919a_jpgs/...`
            --> `2018/09/19`) and `size` is determined by Python's `os.path.getsize()` function.
