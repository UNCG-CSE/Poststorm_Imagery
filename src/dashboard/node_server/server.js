//---Modules and Const---
const express = require("express");
const app = express();
const path = require('path');
const fs = require('fs');

const DIR = path.join(__dirname, '');
const DIR_DATA = path.join(__dirname, 'data');
const PORT=4000
const IP='35.239.226.117:4000'
const IMAGE_ROUTE='photos'
const IMAGE_FOLDER='data'

//---START---
//??? possibly okay to remove
app.use(express.static(DIR));

//This variable to used to keep track of all images that have a route.
let image_list=[];

//Generate routs for all images in file
fs.readdir(DIR_DATA, function (err, files) {
    //handling error,??? does this even work lol
    if (err) {
        return console.log('Unable to scan directory: ' + err);
    } 

    //listing all files using forEach
    files.forEach(function (file) {
        
        //Get the file name without extension.
        const file_name=file.split('.').slice(0, -1).join('.')
        const file_ext=file.split('.')[1]
        const file_route=IMAGE_ROUTE+'/'+file_name
        const file_path=IMAGE_FOLDER+'/'+file
        const file_url='http://'+IP+'/'+file_route
        //Add that to the list of images with routes
        let image_route={
            file_name:file_name,
            file_ext:file_ext,
            file_route:file_route,
            file_url:file_url

        }
        image_list.push(image_route)

        //Create a route with that images name,and send that file.
        app.get(file_route, (req, res, next) => {
            res.sendFile(path.resolve(path.resolve(__dirname,file_path)));
        });
    });
});

//Return a randomly selected image data
app.get("/", (req, res, next) => {
    const selected_img=image_list[Math.floor(Math.random()*image_list.length)]
    res.json(
        selected_img
    )
});

//---Start Server---
//Used to indicate where on terminal server starts
console.log('---SERVER START---')
//Start the server on PORT and make sure it uses the machines IP and not localhost loopback ip.
app.listen(PORT,'0.0.0.0', () => {
    //Use template literalls
    console.log(`Server running on port ${PORT}`);
});