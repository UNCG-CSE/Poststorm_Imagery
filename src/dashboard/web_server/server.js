//---Modules and Const---
const express = require('express')
const app_express = express();
const next = require('next')

const PORT=3000

const dev = process.env.NODE_ENV !== 'production'
const app_next = next({ dev })
const handle = app_next.getRequestHandler()

//---START---
app_next.prepare()
.then(() => {

    //For any requests, let Next.Js handle it
    app_express.get('*', (req, res) => {
        return handle(req, res)
    })

    //have the server listen on PORT and use machines IP>
    app_express.listen(PORT,'0.0.0.0', (err) => {
        console.log(`> Ready on http://localhost:${PORT}`)
    });
})
.catch((ex) => {
    console.error(ex.stack)
    process.exit(1)
})