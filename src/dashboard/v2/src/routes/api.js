const express = require('express');
require("dotenv").config();
//const app = express();
const router = express.Router();
const request = require("request");
const fs = require('fs');
const auth0Token = require("../components/getBearerToken");

const axios = require('axios');

//For running python scripts
const {PythonShell}=  require ('python-shell');

const assignerScript='assign.py';
const assignerSrc='../../python/psic/assigner/';//'./src/routes/'; //
const imageSource='/home/namenai/P-Sick/'

// mattm specific test config
// const fullSizeImagePath='F:\\Shared drives\\P-Sick\\data\\Florence';
// const smallSizeImagePath='F:\\Shared drives\\P-Sick\\small\\Florence';

// namenai specific test config
const fullSizeImagePath='/home/namenai/P-Sick/data/Florence';
const smallSizeImagePath='/home/namenai/P-Sick/small/Florence';

const possible_developmentGroup_tags =[
    'DevelopedId',
    'UndevelopedId'
]
const possible_washoverVisibilityGroup_tags =[
    'VisibleWashoverId',
    'NoVisibleWashoverId'
]
const possible_impactGroup_tags =[
    'SwashId',
    'OverwashId',
    'InundationId',
    'CollisionId'
]
const possible_terrianGroup_tags =[
    'RiverId',
    'MarshId',
    'SandyCoastlineId'
]

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

    //Python stuff
    router.post('/getImage', async function (req, res) {

        try {
            res.setHeader('Access-Control-Allow-Origin', '*');
            const {userId}=req.body;

            // Options to get the user's current image
            let options = {
                mode: 'text',
                pythonOptions: ['-u'], // get print results in real-time
                scriptPath: './',
                //pythonPath:'home/namenai/Documents/GitKraken/Poststorm_Imagery/src/python',
                args: [
                    'current',
                    `-p`, fullSizeImagePath,
                    `-s`, smallSizeImagePath,
                    `-u`, userId
                ]
            };

            PythonShell.run(`${assignerSrc}${assignerScript}`, options, function (err, results) {
                if (err) throw err;

                const parsed_result=JSON.parse(results)

                console.log('Parsed from python assinger',parsed_result)

                //Get the contents of json
                const {
                    original_size_path:original_path,
                    small_size_path:small_path
                }=parsed_result.content

                //Remove the parts that we dont need,everything left of 'P-Sick'
                const full_image_path=original_path.split('P-Sick').slice(-1)[0]
                const small_image_path=small_path.split('P-Sick').slice(-1)[0]

                const image_id=full_image_path.split('data').slice(-1)[0]


                return_json ={
                    full_image_path:full_image_path,
                    small_image_path:small_image_path.replace('data','small'),
                    image_id:image_id
                }
                res.send(return_json)
            });


        } catch(error){
            res.send({})
        }

    });

    //example data/Florence/20180920b_jpgs/jpgs/C26356183.jpg
    //https://stackoverflow.com/questions/15128849/using-multiple-parameters-in-url-in-express
    router.get('/:folder/:storm/:archive/:imageType/:imageFile', function (req, res,next) {
        const {storm,archive,imageType,imageFile,folder} = req.params;

        const file_route=`${imageSource}${folder}/${storm}/${archive}/${imageType}/${imageFile}`
        console.log(file_route)
        const options = {
            root: '/',
            dotfiles: 'allow',
            headers: {
              'x-timestamp': Date.now(),
              'x-sent': true
            }
        }

        try {

            //file exists
            res.sendFile(file_route, options, function (err) {
                //error catching http://expressjs.com/en/4x/api.html#res.sendFile
                if (err) {
                    //need so that node can handle
                    //res.status(404).send("Sorry! You can't see that.")
                    next(err)
                } else {
                    console.log(`Sent: ${file_route} time: ${options.headers['x-timestamp']}`)
                }
            })

        } catch(err) {
            console.error(err)
            next()
        }

        // res.send({
        //     x:[storm,archive,imageType,imageFile]
        // })






    });

    router.post('/submit_image_tags', function (req, res) {
        res.setHeader('Access-Control-Allow-Origin', '*');
        try {
            const {
                developmentGroup,
                washoverVisibilityGroup,
                impactGroup,
                terrianGroup,
                additional_notes,
                image_id,
                user_id
            } = req.body
            console.log(req.body)

            if(user_id && developmentGroup && washoverVisibilityGroup && impactGroup && terrianGroup && image_id) {
                //Now to check the passed in data.
                const devGroupCheck=[developmentGroup].every(val => possible_developmentGroup_tags.includes(val))
                const washoverCheck=[washoverVisibilityGroup].every(val => possible_washoverVisibilityGroup_tags.includes(val))
                const impactCheck=[impactGroup].every(val => possible_impactGroup_tags.includes(val))

                //Not sure wat to do or terrianGroup check
                //if any fails
                if( !devGroupCheck || !washoverCheck || !impactCheck) {
                    throw 'Sent invalid tag id'
                }

                //Do insert
                res.send({
                    message:`Image ${image_id} for user ${user_id} has been tagged`
                })

            }
            else
            {
                throw 'Not all tagging data was sent'

            }

        }catch (err){// big error
            console.error(err);
            res.send({
                message:`ERROR - ${err}`
            })
        }

        //res.send('POST request to homepagex')
    })

    router.post('/submit_ocean_image', function (req, res) {
        res.setHeader('Access-Control-Allow-Origin', '*');
        try {
            const {
                image_id,
                user_id
            } = req.body
            console.log(req.body)

            if(user_id && image_id) {

                let options = {
                    mode: 'text',
                    pythonOptions: ['-u'],
                    scriptPath: './',
                    args: [
                        'tag',
                        'next',
                        `-p`, fullSizeImagePath,
                        `-s`, smallSizeImagePath,
                        `-u`, user_id,
                        `--ocean`
                    ]
                };

                PythonShell.run(`${assignerSrc}${assignerScript}`, options, function (err, results) {
                    if (err) throw err;

                    const parsed_result=JSON.parse(results)

                    console.log('Parsed from python assinger',parsed_result)

                    res.send({
                        message:`Image ${image_id} for user ${user_id} has been tagged as ocean`
                    })    
                });

                // //Do insert
                // res.send({
                //     message:`Image ${image_id} for user ${user_id} has been tagged as ocean`
                // })

            }
            else
            {
                throw 'Image ID not sent'
            }

        }catch (err){// big error
            console.error(err);
            res.send({
                message:`ERROR - ${err}`
            })
        }

        //res.send('POST request to homepagex')
    })

    router.post('/skip_image', async function (req, res) {

        try {
            res.setHeader('Access-Control-Allow-Origin', '*');
            const {
                user_id,
                image_id
            }=req.body;
            if(user_id && image_id) {
                
            
                // Options to get the user's current image
                let options = {
                    mode: 'text',
                    pythonOptions: ['-u'],
                    scriptPath: './',
                    args: [
                        'tag',
                        'skip',
                        `-p`, fullSizeImagePath,
                        `-s`, smallSizeImagePath,
                        `-u`, user_id
                    ]
                };

                PythonShell.run(`${assignerSrc}${assignerScript}`, options, function (err, results) {
                    if (err) throw err;

                    const parsed_result=JSON.parse(results)

                    console.log('Parsed from python assinger',parsed_result)

                    res.send({
                        message:`Image ${image_id} for user ${user_id} skipped :)`
                    })
                });

            }
            else {
                throw 'Incomplete data sent'
            }




        } catch (err){// big error
            console.error(err);
            res.send({
                message:`ERROR - ${err}`
            })
        }

    });

}
main();

//used below becuase https://stackoverflow.com/questions/27465850/typeerror-router-use-requires-middleware-function-but-got-a-object
module.exports = router ;
