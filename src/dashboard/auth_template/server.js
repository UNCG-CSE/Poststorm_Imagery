//---Modules and Const--- wowe
const express = require('express')
const app_express = express();
const next = require('next')

//this contains the secrect wowe
if (process.env.NODE_ENV !== 'production') {
    require('dotenv').config()
}

//for auth 
const bcrypt= require('bcrypt')
//const flash = require('express-flash')
const session = require('express-session')
const initializePassport = require('./passport-config')
const passport =  require('passport')
const methodOverride = require('method-override')

initializePassport(passport,
    email => users.find(user => user.username === email),
    id => users.find(user => user.id === id)
)

//this is our psudo DB
const users =[
    { 
        id: '1570311798516',
        username: 'a',
        password:'$2b$10$JAC9mennQRajf4mBseuYAOD5UfQDktlEP.4fX3qyJU6/xTyUYvZfG' 
    }
]

app_express.use(express.urlencoded({extended: false}))
//enc all information,wowe
app_express.use(session({
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false
}))
app_express.use(passport.initialize())
app_express.use(passport.session())
app_express.use(methodOverride('_method'))

//allow to get post data json
app_express.use(express.json());

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

        app_express.post(
            '/loginUser',  
            passport.authenticate('local'),
            function(req, res) {
                //res.redirect('/')
                res.send({
                    redirect:'/'
                })
            }
        )

        app_express.post("/registerUser",async (req,res) => {
            try {
                const password=req.body.password
                const username=req.body.username
                const hashedPassword = await bcrypt.hash(password, 10)
                users.push({
                    id: Date.now().toString(),
                    username: username,
                    password: hashedPassword
                })
                res.send('user created')
               
            } catch(err) {
                res.send(err.message)
                //res.redirect('/register')
            }
            console.log(users)
        })

        //protected path
        app_express.get("/protected",checkAuthenticated, (req,res) => {
            console.log('woweeeeeeeeeeeeeeeeeeee')
            return handle(req, res)
        })
        
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

function checkAuthenticated(req, res, next) {
    console.log('IS AUTH:',req.isAuthenticated())
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