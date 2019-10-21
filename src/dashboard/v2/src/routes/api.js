const express = require('express');
require("dotenv").config();
//const app = express();
const router = express.Router();
const request = require("request");
const auth0Token = require("../components/getBearerToken");

//For running python scripts
const {PythonShell}=  require ('python-shell');

const assignerScript='assign.py';
const assignerSrc='../../python/psic/assigner/';//'./src/routes/'; //

// mattm specific test config
// const fullSizeImagePath='F:\\Shared drives\\P-Sick\\data\\Florence';
// const smallSizeImagePath='F:\\Shared drives\\P-Sick\\small\\Florence';

// namenai specific test config
const fullSizeImagePath='/home/namenai/P-Sick/data/Florence';
const smallSizeImagePath='/home/namenai/P-Sick/small/Florence';



async function  main() {
    const BEARER= await auth0Token.getAuth0Token();

    router.use('/test', function (req, res) {
        res.json(
            {
                test_api:'WOWE, test api.',
                test_IP:5,
                test_rng:Math.random(),
                test_api_ver:'1.0'
            }
        )
    });

    router.get('/getUserRole/:user_id', function (req, res) {
        //google-oauth2|100613204270669384478

        const {user_id} = req.params;
        const getRoleByUserOptions = {
          method: 'GET',
          url: `https://${process.env.AUTH0_DOMAIN}/api/v2/users/${user_id}/roles`,
          //qs: {q: 'email:"sarafiqu@uncg.edu"', search_engine: 'v3'},
          headers: {authorization: `Bearer ${BEARER}`}
        };

        request(getRoleByUserOptions, function (error, response, body) {
            if (error) throw new Error(error);
            //console.log(JSON.parse(body))
            res.json(
                {
                    data:JSON.parse(body)
                }
            )
        });

    });

    router.get('/getTaggableStorms', function (req, res) {
        const storm_choices=[
            {
                label:"Florence (2018)", value:1
            }
        ];
        res.send({
            storms:storm_choices
        });

    });

    router.post('/getImage', async function (req, res) {
        //allow json to be sent
        res.setHeader('Access-Control-Allow-Origin', '*');
        const {userId}=req.body;
        let responseJson='XX';
        //lets run py in js

        // Options to get the user's current image
        let options = {
            mode: 'text',
            pythonOptions: ['-u'], // get print results in real-time
            scriptPath: './',
            args: [
                'current',
                `-p`, fullSizeImagePath,
                `-s`, smallSizeImagePath,
                `-u`, userId
            ]
        };
        console.log(`getImage > Using args: [${options.args}]`);



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


        PythonShell.run(`${assignerSrc}${assignerScript}`, options, function (err, results) {
            if (err) throw err;
            // results is an array consisting of messages collected during execution
            console.log('>>>>>>>> results: %j', results);
            res.send(`User id: ${userId} and res: ${results}`)
        });


    });

    router.post('/stormToTag', function (req, res) {
        res.setHeader('Access-Control-Allow-Origin', '*');
        console.log(req.body);
        res.send('POST request to homepagex')
    })

}
main();

//used below becuase https://stackoverflow.com/questions/27465850/typeerror-router-use-requires-middleware-function-but-got-a-object
module.exports = router ;
