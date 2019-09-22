//Used to get the IP of the machine
const public_ip = require('public-ip');

//These are our command line arguments that we will accept
const optionDefinitions = [
    { name: 'localhost', alias: 'l', type: Boolean }
]
const commandLineArgs = require('command-line-args')
const options = commandLineArgs(optionDefinitions)

//Get the command line args,and default to true of undef.
const USE_LOCALHOST=options.localhost || true

//export out variables
module.exports = (async function() {

    //Depending on the command line arg, use localhost or machine IP
    //This is so that the web server and node server 
    const IP = USE_LOCALHOST?  'localhost':await public_ip.v4()

    //Becuase the website and server will have diff ports.
    const PORT_WEB=3000
    const PORT_NODE=4000

    //Following the above comment,we need to generate diff ips with diff ports.
    const SITE_IP = {
        node: `${IP}:${PORT_NODE}`,
        web: `${IP}:${PORT_WEB}`
    }

    //Yeet these vars out so export can export.
    return { 
        IP,
        PORT_WEB ,
        PORT_NODE,
        SITE_IP
    };

})();
