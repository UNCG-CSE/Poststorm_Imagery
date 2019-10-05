//---Modules and Const--- wowe
const express = require('express')
const app_express = express();
const next = require('next')
const config = require('./server_config')
const bodyParser = require('body-parser');

//Next.js stuff.
const dev = process.env.NODE_ENV !== 'production'
const app_next = next({ dev })
const handle = app_next.getRequestHandler()
app_next.setAssetPrefix('')//http://cdn.com/myapp

//So that w can use json
app_express.use(bodyParser.urlencoded({ extended: true }));
app_express.use(bodyParser.json());

//Our 'DB'
const users=[]

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

        app_express.post("/createUser",async (req,res) => {
            res.setHeader('Access-Control-Allow-Origin', '*');
            try{
                const hashedPassword = await bcrypt.hash(req.body.password, 10)
                const newUser={
                    id: Date.now().toString(),
                    name: req.body.name,
                    password: req.body.password
                }
                users.push(newUser)
                console.log( newUser)
            
            res.send('User created :)')

            } catch(err) {
                res.send('failed')
            }
            
        })

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