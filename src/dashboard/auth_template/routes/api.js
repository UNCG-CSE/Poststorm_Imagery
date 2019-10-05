const express = require('express');
const app_express = express()
const router = express.Router();
const config = require('../server_config')
const bodyParser = require('body-parser');
const NextRouter = require ('next/router')


const users=[]

//auth
const bcrypt= require('bcrypt')
const flash = require('express-flash')
const session = require('express-session')
const initializePassport = require('../passport-config')
const passport =  require('passport')
const methodOverride = require('method-override')

initializePassport(passport,
    email => users.find(user => user.email === email),
    id => users.find(user => user.id === id)
)

async function main() {
    const {IP} = await config

    //App setttings
    router.use(express.urlencoded({extended: false}))
    router.use(flash())
    //enc all information,wowe
    router.use(session({
        secret: 'ahhhhhhhh',
        resave: false,
        saveUninitialized: false
    }))
    router.use(passport.initialize())
    router.use(passport.session())
    router.use(methodOverride('_method'))
    
    //router.use(express.json());
    router.use(bodyParser.urlencoded({ extended: true }));
    router.use(bodyParser.json());

    //app_express.use(express.json());
    app_express.use(bodyParser.urlencoded({ extended: true }));
    app_express.use(bodyParser.json());

    router.use('/test', function (req, res) {
        res.json(
            {
                test_api:'WOWE, test api. 😊.',
                test_IP:IP,
                test_rng:Math.random(),
                test_api_ver:'1.0'
            }
        )
    });

    router.post('/login',  checkNotAuthenticated,passport.authenticate('local', {
        successRedirect: '/',
        failureRedirect: '/login',
        failureFlash: true
    }))

    // router.post("/login",async (req,res) => {
    //     //res.redirect('/')

    //     res.send({
    //         goaway:'/'
    //     })
    // })


    router.post("/register",async (req,res) => {
        res.setHeader('Access-Control-Allow-Origin', '*');
        try {
            const {password,email}=req.body

            if(password ===undefined){
                throw Error('Password is undefined')
            }
            if(email ===undefined){
                throw Error('Email is undefined')
            }

            const hashedPassword = await bcrypt.hash(password, 10)

            users.push({
                id: Date.now().toString(),
                email: email,
                password: hashedPassword
            })
            
            res.send('User created :)')
            
        } catch (err){
            //res.redirect('/register')
            console.log(err.message)
            res.send(err.message)
        }
        console.log(users)
        console.log('\n\n')
    })

    //protected path
    router.get("/protec",checkAuthenticated, (req,res) => {
        res.send({isProtec:'yes :)'})
    })

    //unprotected path
    router.get("/unprotec",(req,res) => {
        res.send({isProtec:'no :('})
    })

}
main()

function checkAuthenticated(req, res, next) {
    //if authed, then continue
    if (req.isAuthenticated()) {

      return next()
    }

    //if not auth,get yeeted
    res.redirect('/login')
}

//if someone is logged in, move em to the first logged in page
function checkNotAuthenticated(req, res, next) {
    if (req.isAuthenticated()) {
        
      return res.redirect('/')
      
    }
    
    next()
}

//used below becuase https://stackoverflow.com/questions/27465850/typeerror-router-use-requires-middleware-function-but-got-a-object
module.exports = router ;