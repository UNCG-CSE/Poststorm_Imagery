//---Modules and Const--- wowe
const express = require('express')
const app_express = express();
const config = require('./server_config')

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
        PORT_NODE,
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

    //Routes
    app_express.get('/', function (req, res) {
        res.send('Hello there 👋')
    })

     //Notify that the node server is up,and where.
    app_express.listen(PORT_NODE,'0.0.0.0', () => {
        console.log(`>>> Website ready on ${SSL}${SITE_IP.node} `)
    });

  
}


//Run
main()