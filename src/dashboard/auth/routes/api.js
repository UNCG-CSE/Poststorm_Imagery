const express = require('express');
const app_express = express()
const router = express.Router();
const config = require('../server_config')
const bodyParser = require('body-parser');


const users=[]
const bcrypt= require('bcrypt')
async function main() {
    const {IP} = await config
    
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
            //res.redirect('/login')
        } catch (err){
            //res.redirect('/register')
            console.log(err.message)
            res.send(err.message)
        }
        console.log(users)
        console.log('\n\n')
    })
}
main()

//used below becuase https://stackoverflow.com/questions/27465850/typeerror-router-use-requires-middleware-function-but-got-a-object
module.exports = router ;