  // // Get the user's next image (when they press Skip, after tags are saved)
    //     args: [
    //         'tag', 'skip',
    //         `-p`, fullSizeImagePath,
    //         `-s`, smallSizeImagePath,
    //         `-u`, userId
    //     ]
    //
    // // Get the user's next image (when they click Submit, after tags are saved)
    //     args: [
    //         'tag', 'next',
    //         `-p`, fullSizeImagePath,
    //         `-s`, smallSizeImagePath,
    //         `-u`, userId
    //     ]
    //
    // // Submit a multiple choice response with only 1 possibility (they selected one of the choices)
    // // - In cases where multiple choices cannot be selected at the same time, the options should
    // //   be incremented from 0 (0 = first option, 1 = second, 2 = third) such that only one can
    // //   be set at a time.
    // // - This will update any existing value with the new one passed as optionChoice (type: int)
    //     args: [
    //         'tag', 'add',
    //         `-p`, fullSizeImagePath,
    //         `-s`, smallSizeImagePath,
    //         `-u`, userId,
    //         `-t`, tagID,         // The tag id (e.g. 'development')
    //         `-c`, tagContent     // The choice as an integer to set the tag to (e.g. 0 = undeveloped, 1 = developed)
    //     ]
    //
    // // tagID = 'development':
    // // - tagContent: '0' = undeveloped, '1' = developed
    // //
    // // tagID = 'wash-over':
    // // - tagContent: '0' = no wash-over, '1' = visible wash-over
    // //
    // // tagID = 'storm_impact':
    // // - tagContent: '0' = swash, '1' = collision, '2' = over-wash, '3' = inundation
    //
    // // Submit a TRUE / FALSE value tag as TRUE (they CHECK a checkbox or one sub-option of a multiple selections option)
    // // - Multiple choice selections should each be considered their own true / false tag
    // // - Choices where there is multiple options, but the user can only choose one should NOT be handled
    // //   as separate tags, though!
    //     args: [
    //         'tag', 'add',
    //         `-p`, fullSizeImagePath,
    //         `-s`, smallSizeImagePath,
    //         `-u`, userId,
    //         `-t`, tagID
    //     ]
    //
    // // Possible tagIDs = 'terrain_river', 'terrain_marsh', 'terrain_sandy_coastline', ???> 'terrain_water_only' <???
    //
    // // Submit additional text-based response (user has typed something in the 'Additional Notes' section)
    //     args: [
    //         'tag_notes',
    //         `-p`, fullSizeImagePath,
    //         `-s`, smallSizeImagePath,
    //         `-u`, userId,
    //         `-c`, comment  // The notes the user left for the current image (e.g. 'Wowe')
    //     ]
    // // Comment: A string of any length (preferably enforce some length limit on front-end)
