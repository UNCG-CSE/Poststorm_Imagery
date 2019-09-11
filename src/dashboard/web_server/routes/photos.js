const express = require('express');
const app = express();
const router = express.Router();
const path = require('path');

const DIR_DATA = path.join(__dirname, 'data');
const IMAGE_FOLDER='data'

router.use('/:image_name', function (req, res, next) {
    //console.log(req)
    const {image_name} = req.params
    const file_path=`${IMAGE_FOLDER}/${image_name}`
    const file_route=`${file_path}`//path.resolve(path.resolve(__dirname,file_path))
    
    var options = {
        //??????
        root: './',//path.join(__dirname, file_path),
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

//used below becuase https://stackoverflow.com/questions/27465850/typeerror-router-use-requires-middleware-function-but-got-a-object
module.exports = router ;