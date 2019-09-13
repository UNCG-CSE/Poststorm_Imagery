const express = require('express');
const app = express();
const router = express.Router();
const path = require('path');
const fs = require('fs');





async function main() {
  const CONSTANTS = await require('../server_constants')
  const {SITE_IP} = CONSTANTS
  const IMAGE_FOLDER='data'
  const image_list=await fs.readdirSync(IMAGE_FOLDER)
  const SCRIPT_NAME = path.basename(__filename).split('.').slice(0, -1).join('.');
  
  // fs.readdirSync('./data').forEach(file => {
  //   //console.log(file);
  // });

  router.use('/get_image', function (req, res, next) {
    const selected_img=image_list[Math.floor(Math.random()*image_list.length)]
    const img_url=`http://${SITE_IP}/${SCRIPT_NAME}/${selected_img}`
    res.json(
        {
          url:img_url,
          file_name:selected_img,
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
      const options = {
          root: './',
          dotfiles: 'allow',
          headers: {
            'x-timestamp': Date.now(),
            'x-sent': true
          }
      }
      
      try {
        if (fs.existsSync(file_path)) {
          //file exists
          res.sendFile(file_route, options, function (err) {
            //error catching http://expressjs.com/en/4x/api.html#res.sendFile
            if (err) {
              //need so that node can handle 
              //res.status(404).send("Sorry! You can't see that.")
              next(err)
            } else {
              console.log(`Sent: ${file_route} time: ${options.headers['x-timestamp']}`)
            }
          })
        }
        else {
          next()  
        }
      } catch(err) {
        console.error(err)
        next()
      }
  
  });
}





//used below becuase https://stackoverflow.com/questions/27465850/typeerror-router-use-requires-middleware-function-but-got-a-object
main()
module.exports = router ;