//---Modules and Const--- wowe
const express = require('express')
const app_express = express();
const bodyParser = require('body-parser');
const yargs = require('yargs').argv



//---START---
async function main() {
    //First lets get the global constants.
    const CONSTANTS = await require('./server_constants')
    const {PORT_NODE,SITE_IP} = CONSTANTS

    app_express.use(bodyParser.urlencoded({ extended: false }));
    app_express.use(express.json());
    
    //For these routes (and sub routes that partical match), use these files for routing.
    app_express.use('/images', require('./routes/images'))
    app_express.use('/test', require('./routes/test'))

    app_express.use(function(req, res, next) {
        res.header("Access-Control-Allow-Origin", "*");
        res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
        next();
    });

    //Finally use this for when use lands to '/'
    app_express.get('/', function (req, res) {
        res.send('Hello there 👋')
    })


    app_express.post('/form_submit', function (req, res) {
        res.setHeader('Access-Control-Allow-Origin', '*');
        console.log(req.body)
        res.send('POST request to homepagex')
    })
    
    // app_express.all('*',function(req,res,next)
    // {
    //     if (!req.get('Origin')) return next();

    //     res.set('Access-Control-Allow-Origin','http://localhost:4000');
    //     res.set('Access-Control-Allow-Methods','GET,POST');
    //     res.set('Access-Control-Allow-Headers','X-Requested-With,Content-Type');

    //     if ('OPTIONS' == req.method) return res.sendStatus(200);

    //     next();
    // });
    //console.log(await axios.get('/user?ID=12345'))
    
    //Notify use that things are ready to go.
    app_express.listen(PORT_NODE,'0.0.0.0', (err) => {
        console.log(`> Node server ready on http://${SITE_IP.node}`)
    });

  
}


//Run
main()