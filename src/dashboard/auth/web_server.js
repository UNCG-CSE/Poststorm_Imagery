//---Modules and Const--- wowe
const express = require('express')
const app_express = express();
const next = require('next')
const PORT_WEB=3000
//---START---
async function main() {  
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
        app_express.listen(PORT_WEB,'0.0.0.0', () => {
            console.log(`>>> Website ready on http://localhost:${PORT_WEB}`)
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