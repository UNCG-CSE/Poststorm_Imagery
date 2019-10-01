const express = require('express');
//const app = express();
const router = express.Router();
let CONSTANTS=
(async () => {
    CONSTANTS= await require('../server_constants')
    Object.freeze(CONSTANTS)
})();

router.use('/routes', (req, res) => {
    res.json(
        {routes:router.stack}
    )
})

router.use('/', function (req, res) {
    res.json(
        {
            test_api:'WOWE, test api.',
            test_IP:CONSTANTS.IP,
            test_rng:Math.random(),
            test_api_ver:'1.0'
        }
    )
});



//used below becuase https://stackoverflow.com/questions/27465850/typeerror-router-use-requires-middleware-function-but-got-a-object
module.exports = router ;