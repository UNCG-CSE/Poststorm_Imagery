//---Modules and Const--- wowe
const express = require('express')
const app_express = express();
const next = require('next')
const path = require('path');
const fs = require('fs');
const public_ip = require('public-ip');
const util = require('util');

const PORT=3000
const DIR = path.join(__dirname, '');
const DIR_DATA = path.join(__dirname, 'data');
const READDIR = util.promisify(fs.readdir);

const IMAGE_ROUTE='photos'
const IMAGE_FOLDER='data'

let IP = '35.239.226.117'
let SITE_IP = `${IP}:${PORT}`

const dev = process.env.NODE_ENV !== 'production'
const app_next = next({ dev })
const handle = app_next.getRequestHandler()

//This variable to used to keep track of all images that have a route.
let image_list=[];

//---START---

async function main() {
    IP=await public_ip.v4()//'35.239.226.117:'+PORT
    SITE_IP=IP+':'+PORT
    Object.freeze(IP)
    Object.freeze(SITE_IP)
    app_next.setAssetPrefix('')//http://cdn.com/myapp
    app_next.prepare()
    .then(async () => {
        
      
        //Generate routs for all images in file
        //await gen_image_routes()
        
        // app_express.use('/subapp', function (req, res, next) {
        //     res.json(
        //         {  
        //             test_rng:Math.random(), 
        //         }
        //     )
        // });

        app_express.use('/images', require('./routes/photos'))
        app_express.use('/test', require('./routes/test_api'))

        //For any requests, let Next.Js handle it. 
        //Put this after all custom routes so that Next js knows not to error that route
        console.log('before get')    
        app_express.get('*', (req, res) => {
            return handle(req, res)
        })
            
    
        //have the server listen on PORT and use machines IP
        app_express.listen(PORT,'0.0.0.0', (err) => {
            console.log(`> Ready on ${IP}:${PORT}`)
        });

        show_routes()
    })
    .catch((ex) => {
        console.error(ex.stack)
        process.exit(1)
    })
}

async function gen_image_routes(){
   return new Promise(async (resolve, reject) => {
        READDIR(DIR_DATA,async function (err, files) {
            //handling error,??? does this even work lol
            if (err) {
                return console.log('Unable to scan directory: ' + err);
            } 
            //listing all files using forEach
            files.forEach(function (file) {
            
                //Get the file name without extension.
                const file_name=file.split('.').slice(0, -1).join('.')
                const file_ext=file.split('.')[1]
                const file_route='/'+IMAGE_ROUTE+'/'+file_name
                const file_path=IMAGE_FOLDER+'/'+file
                const file_url='http://'+SITE_IP+file_route
                
                //Add that to the list of images with routes
                let image_route={
                    file_name:file_name,
                    file_ext:file_ext,
                    file_route:file_route,
                    file_url:file_url
                }
                image_list.push(image_route)
                //console.log(image_route)
                console.log(file_name)
                //Create a route with that images name,and send that file.
                app_express.get(file_route, (req, res, next) => {
                    res.sendFile(path.resolve(path.resolve(__dirname,file_path)));
                });
            });
         
            //Make a route to get a random image
            app_express.get('/get_image', (req, res) => {
                const selected_img=image_list[Math.floor(Math.random()*image_list.length)]
                res.json(
                    selected_img
                )
            })
            resolve("done!")
        });
    }); 
}


async function show_routes()
{   
    console.log(app_express._router.stack)
}

main()