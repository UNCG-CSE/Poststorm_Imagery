const public_ip = require('public-ip');

module.exports = (async function() {

    const IP = await public_ip.v4()
    const PORT_WEB=3000
    const PORT_NODE=4000
    const SITE_IP = {
        node: `${IP}:${PORT_NODE}`,
        web: `${IP}:${PORT_WEB}`
    }
    async function show_routes(args={})
    {   
        console.log(app_express._router.stack)
        
    }
    return { 
        IP,
        PORT_WEB ,
        PORT_NODE,
        SITE_IP,
        show_routes
    };

})();
