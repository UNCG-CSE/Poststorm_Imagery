const express = require('express');
require("dotenv").config();
//const app = express();
const router = express.Router();
const request = require("request");
const fs = require('fs');
const auth0Token = require("../components/getBearerToken");

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
                // results is an array consisting of messages collected during execution
                const parsed_result=JSON.parse(results)
                console.log(parsed_result)
                // const {original_size_path:original_path}=parsed_result.content
                // const splitted=original_path.split('\\P-Sick\\')
                // const sliced_image_path=splitted.slice(-1)[0].replace('\\','/')
                // const image_path_final=`${imageSource}${sliced_image_path}`
                //x=/home/namenai/P-Sick/data/Florence/20180920b_jpgs/jpgs
                //versus=/home/namenai/Documents/GitKraken/Poststorm_Imagery/src/dashboard/v2/F:\\Shared drives\\P-Sick\\data\\Florence/20180920b_jpgs/jpgs/C26356183.jpg',
                //console.log(image_path_final)
                res.send(`User id: ${userId}`)
            });
            // res.send(`Wowe:${options.args}`)
            
        } catch(error){
            res.send(`F,error`)
        }

    });

    //example data/Florence/20180920b_jpgs/jpgs/C26356183.jpg
    //https://stackoverflow.com/questions/15128849/using-multiple-parameters-in-url-in-express
    router.get('/data/:storm/:archive/:imageType/:imageFile', function (req, res,next) {
        const {storm,archive,imageType,imageFile} = req.params;

        const file_route=`${imageSource}data/${storm}/${archive}/${imageType}/${imageFile}`
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

    router.post('/stormToTag', function (req, res) {
        res.setHeader('Access-Control-Allow-Origin', '*');
        console.log(req.body);
        res.send('POST request to homepagex')
    })

}
main();

//used below becuase https://stackoverflow.com/questions/27465850/typeerror-router-use-requires-middleware-function-but-got-a-object
module.exports = router ;
