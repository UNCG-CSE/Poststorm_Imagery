//This file is mainly here so that we know to use local or ip address
const public_ip = require('public-ip');
const USELOCAL=true;

module.exports.getIp= async (options) =>  {
	options = {
		...options
  };

  //all Env are strings, so cant do strict typing
  if(USELOCAL){
    return '35.237.34.41';
  }

	return (await public_ip.v4());
};
