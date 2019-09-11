const express = require('express');
const app = express();
const router = express.Router();
const public_ip = require('public-ip');

let IP=
(async () => {
    IP=await public_ip.v4();
    Object.freeze(IP)
})();

router.use('/routes', (req, res) => {
    res.json(
        {routes:app._router}
    )
})

router.use('/', function (req, res, next) {
    res.json(
        {
            test_api:'WOWE, test api.',
            test_IP:IP,
            test_rng:Math.random(),
            test_api_ver:'1.0'
        }
    )
});



//used below becuase https://stackoverflow.com/questions/27465850/typeerror-router-use-requires-middleware-function-but-got-a-object
module.exports = router ;