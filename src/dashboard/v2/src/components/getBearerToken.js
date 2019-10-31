
require("dotenv").config();
const request = require("request");
const rp = require('request-promise');

module.exports.getAuth0Token= async () =>  {
	// options = {
	// 	...options
  // };

  const getTokenOptions = {
      method: 'POST',
      url: `https://${process.env.AUTH0_DOMAIN}/oauth/token`,
      headers: {'content-type': 'application/x-www-form-urlencoded'},
      form: {
          grant_type: 'client_credentials',
          client_id: `${process.env.AUTH0_CLIENT_ID}`,//'Vkl8Cx7XgD3zQY0yusSr5Db2mgh5UT8v',
          client_secret: `${process.env.AUTH0_CLIENT_SECRET}`,//'7sfyqypiGTuxRsKJxyDEbkit7TbtwfCgZsQpbaNTFt7cSMF2sMYubKq72GZvkKAB',
          audience: `https://${process.env.AUTH0_DOMAIN}/api/v2/`
      }
  };

  return await rp(getTokenOptions)
    .then(function (parsedBody) {
        //Request successs
        const payload=JSON.parse(parsedBody)
        return payload.access_token
    })
    .catch(function (err) {
        //Request successs
        console.log(err)
    });





};
