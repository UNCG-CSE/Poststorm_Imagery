const express = require('express');
require("dotenv").config();

const router = express.Router();
const request = require("request");
const auth0Token = require("../components/getBearerToken");

//For running python scripts
const {PythonShell}=  require ('python-shell');

//Location of the python assinger script
const assignerScript='assign.py';
const assignerSrc='../../python/psic/assigner/';//'./src/routes/'; //
const imageSource='/home/namenai/P-Sick/'

//Image incase some error happens
const error_image='https://www.nationwidechildrens.org/-/media/nch/giving/images/on-our-sleeves-1010/icons/icon-teasers/w45084_iconcollectionlandingiconteaserimages_facesad.jpg'

// Path to the images,so that assinger knows wats wat.
const fullSizeImagePath='/home/namenai/P-Sick/data/Florence';
const smallSizeImagePath='/home/namenai/P-Sick/small/Florence';

//Used to take user form inputs and convert over to intergers for tensor flow
const tag_name_value_pairs={
    development:{
        DevelopedId:0,
        UndevelopedId:1
    },
    washover:{
        VisibleWashoverId:0,
        NoVisibleWashoverId:1
    },
    impact:{
        SwashId:0,
        CollisionId:1,
        OverwashId:2,
        InundationId:3,
        
    },
    terrian:{
        RiverId:'RiverId',
        MarshId:'MarshId',
        SandyCoastlineId:'SandyCoastlineId'
    }
}

//Used to validate wat is given for form submition
const possible_developmentGroup_tags =[
    'DevelopedId',
    'UndevelopedId'
]
const possible_washoverVisibilityGroup_tags =[
    'VisibleWashoverId',
    'NoVisibleWashoverId'
]
const possible_impactGroup_tags =[
    'SwashId',
    'OverwashId',
    'InundationId',
    'CollisionId'
]
const possible_terrianGroup_tags =[
    'RiverId',
    'MarshId',
    'SandyCoastlineId'
]

//Used to run python scripts in a sync manner so that we dont have to do promise nesting.
async function runPy(sript_path,callback,options=null){
    return new Promise(function(resolve, reject){
        PythonShell.run(sript_path, options, function (err, results) {
                if (err) throw err;
               
                callback(err, results)
                resolve(results[1])//I returned only JSON(Stringified) out of all string I got from py script
        });
    })
}

//Used to gen tag options for submition since they vary little
function gen_tag_options_submit(user_id,tag_id,tag_content){
    return {
        mode: 'text',
        pythonOptions: ['-u'],
        scriptPath: './',
        args: [
            'tag',
            'add',
            `-p`, fullSizeImagePath,
            `-s`, smallSizeImagePath,
            `-u`, user_id,
            `-t`,tag_id,
            `-c`,tag_content
        ]
    };
}

function gen_comment_options_submit(user_id,comment){
    return {
        mode: 'text',
        pythonOptions: ['-u'],
        scriptPath: './',
        args: [
            'tag',
            'add',
            `-p`, fullSizeImagePath,
            `-s`, smallSizeImagePath,
            `-u`, user_id,
            `-t`,'notes',
            `-c`,comment
        ]
    };
}

function get_next_img_options(user_id){
    return {
        mode: 'text',
        pythonOptions: ['-u'],
        scriptPath: './',
        args: [
            'tag',
            'next',
            `-p`, fullSizeImagePath,
            `-s`, smallSizeImagePath,
            `-u`, user_id
            
        ]
    };
}

//Everything is in an async function becuase sync is good.
async function  main() {
    const BEARER= await auth0Token.getAuth0Token();

    //simple test route 
    router.use('/test', async function (req, res) {

        await runPy('src/routes/test.py',function(err,results){
            console.log(results)
        })
        await runPy('src/routes/test2.py',function(err,results){
            console.log(results)
        })
        res.json(
            {
                test_api:'WOWE, test api.',
                test_IP:5,
                test_rng:Math.random(),
                test_api_ver:'1.0'
            }
        )
    });
    
    //Used to get the users role to prevent non roled ppl from tagging *Currently not used*
    router.get('/getUserRole/:user_id', function (req, res) {
        //google-oauth2|100613204270669384478

        const {user_id} = req.params;
        const getRoleByUserOptions = {
          method: 'GET',
          url: `https://${process.env.AUTH0_DOMAIN}/api/v2/users/${user_id}/roles`,
          //qs: {q: 'email:"sarafiqu@uncg.edu"', search_engine: 'v3'},
          headers: {authorization: `Bearer ${BEARER}`}
        };

        request(getRoleByUserOptions, function (error, response, body) {
            if (error) throw new Error(error);
            //console.log(JSON.parse(body))
            res.json(
                {
                    data:JSON.parse(body)
                }
            )
        });

    });

    //Get list of storms we can tag *Not used*
    router.get('/getTaggableStorms', function (req, res) {
        const storm_choices=[
            {
                label:"Florence (2018)", value:1
            }
        ];
        res.send({
            storms:storm_choices
        });

    });

    //Call the assinger script to get this users (passed in req.body) image
    router.post('/getImage', async function (req, res) {

        try {
            res.setHeader('Access-Control-Allow-Origin', '*');
            const {userId}=req.body;

            // Options to get the user's current image
            let options = {
                mode: 'text',
                pythonOptions: ['-u'], // get print results in real-time
                scriptPath: './',
                //pythonPath:'home/namenai/Documents/GitKraken/Poststorm_Imagery/src/python',
                args: [
                    'current',
                    `-p`, fullSizeImagePath,
                    `-s`, smallSizeImagePath,
                    `-u`, userId
                ]
            };

            PythonShell.run(`${assignerSrc}${assignerScript}`, options, function (err, results) {
                if (err) throw err;

                const parsed_result=JSON.parse(results)

                console.log('Parsed from python assinger',parsed_result)

                if(parsed_result.error_message)
                {
                    throw 'Python script had error'
                }
                //Get the contents of json
                const {
                    original_size_path:original_path,
                    small_size_path:small_path
                }=parsed_result.content

                //Remove the parts that we dont need,everything left of 'P-Sick'
                const full_image_path=original_path.split('P-Sick').slice(-1)[0]
                const small_image_path=small_path.split('P-Sick').slice(-1)[0]

                const image_id=full_image_path.split('data').slice(-1)[0]


                const return_json ={
                    full_image_path:full_image_path,
                    small_image_path:small_image_path.replace('data','small'),
                    image_id:image_id
                }
                res.send(return_json)
            });


        } catch(error){
            res.send({
                full_image_path:error_image,
                small_image_path:error_image,
                image_id:`err`
            })
        }

    });

    //Below comment helped with finding out how to variables in url
    //https://stackoverflow.com/questions/15128849/using-multiple-parameters-in-url-in-express
    router.get('/:folder/:storm/:archive/:imageType/:imageFile', function (req, res,next) {
        const {storm,archive,imageType,imageFile,folder} = req.params;

        const file_route=`${imageSource}${folder}/${storm}/${archive}/${imageType}/${imageFile}`
        console.log(file_route)
        const options = {
            root: '/',
            dotfiles: 'allow',
            headers: {
              'x-timestamp': Date.now(),
              'x-sent': true
            }
        }

        try {

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

        } catch(err) {
            console.error(err)
            next()
        }

        // res.send({
        //     x:[storm,archive,imageType,imageFile]
        // })






    });
    
    //route to submit tags of an image and get next image.
    router.post('/submit_image_tags', async function (req, res) {
        res.setHeader('Access-Control-Allow-Origin', '*');
        try {
            const {
                developmentGroup,
                washoverVisibilityGroup,
                impactGroup,
                terrianGroup,
                additional_notes,
                image_id,
                user_id
            } = req.body
           
            if(user_id && developmentGroup && washoverVisibilityGroup && impactGroup && terrianGroup && image_id) {
                //Now to check the passed in data.
                const devGroupCheck=[developmentGroup].every(val => possible_developmentGroup_tags.includes(val))
                const washoverCheck=[washoverVisibilityGroup].every(val => possible_washoverVisibilityGroup_tags.includes(val))
                const impactCheck=[impactGroup].every(val => possible_impactGroup_tags.includes(val))

                //Not sure wat to do or terrianGroup check
                //if any fails
                if( !devGroupCheck || !washoverCheck || !impactCheck) {
                    throw 'Sent invalid tag id'
                }
                const dev_cat='development'
                const washover_cat='washover'
                const impact_cat='impact'
                const terrian_cat='terrian'

                const dev_value=tag_name_value_pairs[dev_cat][developmentGroup]
                const wash_value=tag_name_value_pairs[washover_cat][washoverVisibilityGroup]
                const impact_value=tag_name_value_pairs[impact_cat][impactGroup]

                console.log(dev_value,wash_value,impact_value,terrianGroup)
   
                await runPy(`${assignerSrc}${assignerScript}`,function(err,results){
                    console.log('development group tag added')
                },gen_tag_options_submit(user_id,dev_cat,dev_value))

                await runPy(`${assignerSrc}${assignerScript}`,function(err,results){
                    console.log('washover group tag added')
                },gen_tag_options_submit(user_id,washover_cat,wash_value))

                await runPy(`${assignerSrc}${assignerScript}`,function(err,results){
                    console.log('impact group tag added')
                },gen_tag_options_submit(user_id,impact_cat,impact_value))

                //How to have looped await, cant use foreach becuase its not promise aware
                //https://zellwk.com/blog/async-await-in-loops/
                const terrian_promise = terrianGroup.map(async element => {

                    return await runPy(`${assignerSrc}${assignerScript}`,function(err,results){
                        const parsed_result=JSON.parse(results)
                        console.log('terrian group tag added')
                    },gen_tag_options_submit(user_id,terrian_cat,true))
                  })
                
                //wait for all terrian tagging to be done
                await Promise.all(terrian_promise)

                console.log('All radio/checkbox tags added')

                await runPy(`${assignerSrc}${assignerScript}`,function(err,results){
                    const parsed_result=JSON.parse(results)
                    console.log('comment added',parsed_result)
                },gen_comment_options_submit(user_id,additional_notes))
                  
                console.log('All tagging data done')
                
                await runPy(`${assignerSrc}${assignerScript}`,function(err,results){
                    console.log('Next image got')
                },get_next_img_options(user_id))

                //Return
                res.send({
                    message:`Image has been tagged, page will refresh to get next image `
                })

            }
            else
            {
                throw 'Not all tagging data was sent'
            }

        }catch (err){// big error
            console.error(err);
            res.send({
                message:`ERROR - ${err}`
            })
        }
    })

    //What to do for the quick option of saying this image is a ocean
    router.post('/submit_ocean_image', async function (req, res) {
        res.setHeader('Access-Control-Allow-Origin', '*');
        try {
            const {
                image_id,
                user_id
            } = req.body

            if(user_id && image_id) {

                let tag_ocean_option = {
                    mode: 'text',
                    pythonOptions: ['-u'],
                    scriptPath: './',
                    args: [
                        'tag',
                        'add',
                        `-p`, fullSizeImagePath,
                        `-s`, smallSizeImagePath,
                        `-u`, user_id,
                        `-t`,`ocean`,`-c`,`true`
                    ]
                };

                let get_next_option = {
                    mode: 'text',
                    pythonOptions: ['-u'],
                    scriptPath: './',
                    args: [
                        'tag',
                        'next',
                        `-p`, fullSizeImagePath,
                        `-s`, smallSizeImagePath,
                        `-u`, user_id
                    ]
                };

                await runPy(`${assignerSrc}${assignerScript}`,function(err,results){
                    console.log('Tagged as ocean')
                },tag_ocean_option)

                await runPy(`${assignerSrc}${assignerScript}`,function(err,results){
                    console.log('Got next image')
                    res.send({
                        message: `Image has been tagged as ocean, page will refresh to get new image`
                    })    
                },get_next_option)
            }
            else
            {
                throw 'Image ID not sent'
            }

        }catch (err){// big error
            console.error(err);
            res.send({
                message:`ERROR - ${err}`
            })
        }
    })

    //skip image quick option
    router.post('/skip_image', async function (req, res) {
        try {
            res.setHeader('Access-Control-Allow-Origin', '*');
            const {
                user_id,
                image_id
            }=req.body;
            if(user_id && image_id) {
                
                // Options to get the user's current image
                let options = {
                    mode: 'text',
                    pythonOptions: ['-u'],
                    scriptPath: './',
                    args: [
                        'tag',
                        'skip',
                        `-p`, fullSizeImagePath,
                        `-s`, smallSizeImagePath,
                        `-u`, user_id
                    ]
                };

                await runPy(`${assignerSrc}${assignerScript}`,function(err,results){
                    console.log('Image skipped')
                    res.send({
                        message: `Image skipped,page will refresh to get new image.`
                    })
                },options)
            }
            else {
                throw 'Incomplete data sent'
            }
        } catch (err){// big error
            console.error(err);
            res.send({
                message:`ERROR - ${err}`
            })
        }
    });
}
main();

//used below becuase https://stackoverflow.com/questions/27465850/typeerror-router-use-requires-middleware-function-but-got-a-object
module.exports = router ;
