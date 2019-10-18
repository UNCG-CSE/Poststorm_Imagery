const express = require('express');
require("dotenv").config();
//const app = express();
const router = express.Router();
const request = require("request");
const auth0Token = require("../components/getBearerToken");


async function  main() {
    const BEARER= await auth0Token.getAuth0Token()

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
        
        const {user_id} = req.params
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
}
main()

//used below becuase https://stackoverflow.com/questions/27465850/typeerror-router-use-requires-middleware-function-but-got-a-object
module.exports = router ;