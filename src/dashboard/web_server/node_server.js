//---Modules and Const--- wowe
const express = require('express')
const app_express = express();

//---START---
async function main() {
    //First lets get the global constants.
    const CONSTANTS = await require('./server_constants')
    const {PORT_NODE,SITE_IP} = CONSTANTS
    
    //For these routes (and sub routes that partical match), use these files for routing.
    app_express.use('/images', require('./routes/images'))
    app_express.use('/test', require('./routes/test'))

    //Finally use this for when use lands to '/'
    app_express.get('/', function (req, res) {
        res.send('Hello there 👋')
    })

    //Notify use that things are ready to go.
    app_express.listen(PORT_NODE,'0.0.0.0', (err) => {
        console.log(`> Node server ready on http://${SITE_IP.node}`)
    });
}

//Run
main()