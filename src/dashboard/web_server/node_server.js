//---Modules and Const--- wowe
const express = require('express')
const app_express = express();

//---START---

async function main() {
    const CONSTANTS = await require('./server_constants')
    const {PORT_NODE,SITE_IP} = CONSTANTS
    
    app_express.use('/images', require('./routes/images'))
    app_express.use('/test', require('./routes/test'))
    app_express.get('/', function (req, res) {
        res.send('Hello there 👋')
    })

    app_express.listen(PORT_NODE,'0.0.0.0', (err) => {
        console.log(`> Node server ready on http://${SITE_IP(PORT_NODE)}`)
    });
}

main()