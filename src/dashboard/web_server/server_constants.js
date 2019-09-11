const public_ip = require('public-ip');

module.exports = (async function() {
 const IP = await public_ip.v4()
 const PORT=3000
 const SITE_IP = `${IP}:${PORT}`
 return { 
     IP,
     PORT ,
     SITE_IP
    };
})();
