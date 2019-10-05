//---Modules and Const--- wowe
const express = require('express')
const app_express = express();
const next = require('next')

//Next.js stuff.
const dev = process.env.NODE_ENV !== 'production'
const app_next = next({ dev })
const handle = app_next.getRequestHandler()
app_next.setAssetPrefix('')//http://cdn.com/myapp

//---START---
async function main() {  
    //Let next.js handle routing
    app_next.prepare()
    .then(async () => { 
        //For all pages use next.js
        app_express.get('*', (req, res) => {
            return handle(req, res)
        })

        //Notify that the web server is up,and where.
        app_express.listen(3000,'0.0.0.0', () => {
            console.log(`>>> Website ready on http://localhost:3000/ `)
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