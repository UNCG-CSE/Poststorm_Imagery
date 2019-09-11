const express = require('express');
const app = express();
const router = express.Router();
const path = require('path');
const fs = require('fs');





async function main() {
  const CONSTANTS = await require('../server_constants')
  const {SITE_IP} = CONSTANTS
  const IMAGE_FOLDER='data'
  const IMAGE_ROUTE='images'
  const image_list=await fs.readdirSync(IMAGE_FOLDER)
  const SCRIPT_NAME = path.basename(__filename);
  
  // fs.readdirSync('./data').forEach(file => {
  //   //console.log(file);
  // });

  router.use('/get_image', function (req, res, next) {
    const selected_img=image_list[Math.floor(Math.random()*image_list.length)]
    const img_url=`${SITE_IP}/${SCRIPT_NAME}/${selected_img}`
    res.json(
        {
          url:img_url,
          time:new Date()
        }
      
    )
  });
  
  router.use('/:image_name', function (req, res, next) {
      //console.log(req)
      const {image_name} = req.params
      const file_path=`${IMAGE_FOLDER}/${image_name}`
      const file_route=`${file_path}`
      //console.log(IP)
      var options = {
          root: './',
          dotfiles: 'allow',
          headers: {
            'x-timestamp': Date.now(),
            'x-sent': true
          }
      }
  
      //erro catching http://expressjs.com/en/4x/api.html#res.sendFile
      res.sendFile(file_route, options, function (err) {
          if (err) {
            console.log(err);
            res.send(`<p>The image <b>'${image_name}'</b> does not exist 😢</p>`)
          }
          else {
            //console.log('Sent:', fileName);
          }
      });
      
  });
}





//used below becuase https://stackoverflow.com/questions/27465850/typeerror-router-use-requires-middleware-function-but-got-a-object
main()
module.exports = router ;