//---Modules and Const--- wowe
const express = require('express')
const app_express = express();
const next = require('next')
const config = require('./server_config')



//Next.js stuff.
const dev = process.env.NODE_ENV !== 'production'
const app_next = next({ dev })
const handle = app_next.getRequestHandler()
app_next.setAssetPrefix('')//http://cdn.com/myapp




//---START---
async function main() {  

    //Lets first get our server config data
    const configData = await config;
    const {
        PORT_WEB,
        SITE_IP,
        SSL
    }=configData;

    //Let next.js handle routing
    app_next.prepare()
    .then(async () => { 

        //For the login page specifly, dont do anything
        app_express.get('/', function (req, res) {
            return handle(req, res)
        })
      
        app_express.use('/api',require('./routes/api'))

        //For all pages use next.js
        app_express.get('*', (req, res) => {
            return handle(req, res)
        })

        //Notify that the web server is up,and where.
        app_express.listen(PORT_WEB,'0.0.0.0', () => {
            console.log(`>>> Website ready on ${SSL}${SITE_IP.web} `)
        });
    })
    .catch((ex) => {
        //Owwwe 😿
        console.error(ex.stack)
        process.exit(1)
    })
}

//Run
main()