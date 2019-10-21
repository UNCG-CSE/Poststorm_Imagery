const express = require('express');
require("dotenv").config();
//const app = express();
const router = express.Router();
const request = require("request");
const auth0Token = require("../components/getBearerToken");

//For running python scripts
const {PythonShell}=  require ('python-shell');

const assignerScript='assign.py';
const assignerSrc='..\\..\\python\\psic\\assigner\\';//'./src/routes/'; //
const fullSizeImagePath='F:\\Shared drives\\P-Sick\\data\\Florence';
const smallSizeImagePath='F:\\Shared drives\\P-Sick\\small\\Florence';



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
                label:"Florence 2018",value:1
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

        //our optionz
        let options = {
            mode: 'text',
            pythonOptions: ['-u'], // get print results in real-time
            scriptPath: '.\\',
            args: ['current',
                `-p`, fullSizeImagePath,
                `-s`, smallSizeImagePath,
                `-u`, userId]
        };
        console.log(`getImage > Using args: [${options.args}]`);


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