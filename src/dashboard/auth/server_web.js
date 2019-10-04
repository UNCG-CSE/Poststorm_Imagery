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

//auth
const bcrypt= require('bcrypt')
const flash = require('express-flash')
const session = require('express-session')
const initializePassport = require('./passport-config')
const passport =  require('passport')
const methodOverride = require('method-override')

initializePassport(passport,
    email => users.find(user => user.email === email),
    id => users.find(user => user.id === id)
)


//---START---
async function main() {  

    //Lets first get our server config data
    const configData = await config;
    const {
        PORT_WEB,
        SITE_IP,
        SSL
    }=configData;

    //App setttings
    app_express.use(express.urlencoded({extended: false}))
    app_express.use(flash())
    //enc all information,wowe
    app_express.use(session({
        secret: 'ahhhhhhhh',
        resave: false,
        saveUninitialized: false
    }))
    app_express.use(passport.initialize())
    app_express.use(passport.session())
    app_express.use(methodOverride('_method'))

    

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