const express = require('express');
const router = express.Router();
const config = require('../server_config')
async function main() {
    const {IP} = await config
    router.use('/routes', (req, res) => {
        res.json(
            {routes:router.stack}
        )
    })
    
    router.use('/', function (req, res) {
        res.json(
            {
                test_api:'WOWE, test api.',
                test_IP:IP,
                test_rng:Math.random(),
                test_api_ver:'1.0'
            }
        )
    });
}
main()


//used below becuase https://stackoverflow.com/questions/27465850/typeerror-router-use-requires-middleware-function-but-got-a-object
module.exports = router ;