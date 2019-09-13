//---Modules and Const--- wowe
const express = require('express')
const app_express = express();
const next = require('next')

//---START---
async function main() {
    //First lets get the global constants.
    const CONSTANTS = await require('./server_constants')
    const {PORT_WEB,SITE_IP} = CONSTANTS
    
    //Next.js stuff.
    const dev = process.env.NODE_ENV !== 'production'
    const app_next = next({ dev })
    const handle = app_next.getRequestHandler()
    app_next.setAssetPrefix('')//http://cdn.com/myapp

    //Let next.js handle routing
    app_next.prepare()
    .then(async () => { 
        //For all pages use next.js
        app_express.get('*', (req, res) => {
            return handle(req, res)
        })

        //Notify user.
        app_express.listen(PORT_WEB,'0.0.0.0', (err) => {
            console.log(`> Website ready on http://${SITE_IP.web}`)
        });
    })
    .catch((ex) => {
        //Owwwe
        console.error(ex.stack)
        process.exit(1)
    })
}

//Run
main()