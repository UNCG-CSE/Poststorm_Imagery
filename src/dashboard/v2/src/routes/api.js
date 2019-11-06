const express = require('express');
require("dotenv").config();

const router = express.Router();
const request = require("request");
const auth0Token = require("../components/getBearerToken");

const chalk = require('chalk');
const serverConfig =require('../server-config')
const log = serverConfig.log
const log_api = api_name => log(`${chalk.yellow(`Running ${chalk.cyan(api_name)} API`)}`)
const log_api_done = api_name =>log(`${chalk.yellow(`${chalk.cyan(api_name)} ${chalk.green(`done`)}`)}`)
const log_api_error = (api_name,err) =>log(`${chalk.red(`ERROR`)} for ${chalk.yellow(`${chalk.cyan(api_name)}`)} API: ${err}`)
const log_img = (image_id,user_name,user_id) => log(`Submitting image ${chalk.cyan(image_id)} for user: ${chalk.yellow(user_name)} aka ${chalk.magenta(user_id)}`)
//For running python scripts
const {PythonShell}=  require ('python-shell');

//Location of the python assigner script
const assignerScript=process.env.ASSIGNER_SCRIPT;
const assignerSrc=process.env.ASSIGNER_SOURCE;
const imageSource=process.env.IMAGE_SOURCE;

//Image in-case some error happens
const error_image='https://www.nationwidechildrens.org/-/media/nch/giving/images/on-our-sleeves-1010/icons/icon-teasers/w45084_iconcollectionlandingiconteaserimages_facesad.jpg'

// Path to the images,so that assinger knows wats wat.
const fullSizeImagePath=process.env.FULL_SIZE_IMAGE_PATH;
const smallSizeImagePath=process.env.SMALL_SIZE_IMAGE_PATH;

//Used to take user form inputs and convert over to intergers for tensor flow
const tag_name_value_pairs={
    development:{
        NoneId:0,
        DevelopedId:1,
        UndevelopedId:2
    },
    washover:{
        NoneId:0,
        VisibleWashoverId:1,
        NoVisibleWashoverId:2
    },
    impact:{
        NoneId:0,
        SwashId:1,
        CollisionId:2,
        OverwashId:3,
        InundationId:4,

    },
    terrian:{
        NoneId:'NoneId',
        RiverId:'RiverId',
        MarshId:'MarshId',
        SandyCoastlineId:'SandyCoastlineId'
    }
}

const terrian_id_tag_pair={
    SandyCoastlineId: 'sandy_coastline',
    MarshId:'marsh',
    RiverId:'river',
    NodeId:'none'
}

//Used to validate wat is given for form submition
const possible_developmentGroup_tags =[
    'DevelopedId',
    'UndevelopedId',
    'NoneId'
]
const possible_washoverVisibilityGroup_tags =[
    'VisibleWashoverId',
    'NoVisibleWashoverId',
    'NoneId'
]

const possible_impactGroup_tags =[
    'SwashId',
    'OverwashId',
    'InundationId',
    'CollisionId',
    'NoneId'
]

const possible_terrianGroup_tags =[
    'RiverId',
    'MarshId',
    'SandyCoastlineId',
    'NoneId'
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

function gen_json_arg(userId,operations){
    return  {
        "py/object": "psic.assigner.batch.Batch",
        "path": fullSizeImagePath,
        "small_path": smallSizeImagePath,
        "user_id": userId,
        "debug": false,
        "operations": [
            ...operations
        ]
    }
}

//Everything is in an async function becuase sync is good.
async function  main() {

    log(`${chalk.yellow(`Getting Bearer token...`)}`)
    const BEARER= await auth0Token.getAuth0Token();
    log(`${chalk.green(`Got`)} ${chalk.yellow(`Bearer token`)}`)

    //simple test route
    router.use('/test', async function (req, res) {
        log_api('/test')
        // const x =  runPy('src/routes/test.py',function(err,results){
        //     console.log(results)
        // })
        // console.log(x)
        // await runPy('src/routes/test2.py',function(err,results){
        //     console.log(results)
        // })
        res.json(
            {
                test_api:'WOWE, test api.',
                test_IP:5,
                test_rng:Math.random(),
                test_api_ver:'1.0',
                test_domain:process.env.BASE_URL
            }
        )
        log_api_done('/test')
    });

    //Used to get the users role to prevent non roled ppl from tagging *Currently not used*
    router.get('/getUserRole/:user_id', function (req, res) {
        //google-oauth2|100613204270669384478
        log_api('/getUserRole/:user_id')
        const {user_id} = req.params;

        log(`${chalk.yellow(`Getting user: ${chalk.cyan(`${user_id || 'N/A'}`)}`)}`)

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
            log_api_done('/getUserRole/:user_id')
        });

    });

    //Get list of storms we can tag *Not used*
    // router.get('/getTaggableStorms', function (req, res) {
    //     const storm_choices=[
    //         {
    //             label:"Florence (2018)", value:1
    //         }
    //     ];
    //     res.send({
    //         storms:storm_choices
    //     });

    // });

    //Call the assinger script to get this users (passed in req.body) image
    router.post('/getImage', async function (req, res) {
        log_api('/getImage')
        try {
            res.setHeader('Access-Control-Allow-Origin', '*');
            const {userId,user_name}=req.body;
            log(`Getting Image for ${chalk.yellow(userId)} aka ${chalk.yellow(user_name)}`)
            const json_args= gen_json_arg(userId,[
                {
                    "command":"current"
                }
            ])

            // Options to get the user's current image
            let options = {
                mode: 'text',
                pythonOptions: ['-u'], // get print results in real-time
                scriptPath: './',
                //pythonPath:'home/namenai/Documents/GitKraken/Poststorm_Imagery/src/python',
                args: [
                    JSON.stringify(json_args)
                ]
            };

            PythonShell.run(`${assignerSrc}${assignerScript}`, options, function (err, results) {
                if (err) throw err;

                const results_content=JSON.parse(results)

                if(results_content.status===1)
                {
                    throw results_content.error_message//'Python script had error'
                }
                //Get the contents of json
                const {
                    original_size_path:original_path,
                    small_size_path:small_path
                }=results_content.content



                //Remove the parts that we dont need,everything left of 'P-Sick'
                const full_image_path=original_path.split('P-Sick').slice(-1)[0]
                const small_image_path=small_path.split('P-Sick').slice(-1)[0]

                const image_id=full_image_path.split('data').slice(-1)[0]

                log(`Got Image ${chalk.cyan(image_id)}`)

                const return_json ={
                    full_image_path:full_image_path,
                    small_image_path:small_image_path.replace('data','small'),
                    image_id:image_id
                }
                res.send(return_json)
                log_api_done('/getImage')
            });


        } catch(error){
            res.send({
                full_image_path:error_image,
                small_image_path:error_image,
                image_id:`err`
            })
            log_api_error('/getImage',error)
        }

    });

    //Below comment helped with finding out how to variables in url
    //https://stackoverflow.com/questions/15128849/using-multiple-parameters-in-url-in-express
    router.get('/:folder/:storm/:archive/:imageType/:imageFile', function (req, res,next) {
        log_api('/:folder/:storm/:archive/:imageType/:imageFile')
        const {storm,archive,imageType,imageFile,folder} = req.params;

        const file_route=`${imageSource}${folder}/${storm}/${archive}/${imageType}/${imageFile}`

        log(`${chalk.yellow(`Getting file: ${chalk.cyan(`${file_route}`)}`)}`)
        //console.log(file_route)
        const options = {
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
                    //f
                    res.send('Image does not exist')
                    log(`Image does not exist`)
                } else {
                    log(`${chalk.cyan(`Image: ${file_route} accessed at time: ${options.headers['x-timestamp']}`)}`)
                    log_api_done(`/${folder}/${storm}/${archive}/${imageType}/${imageFile}`)
                }
            })

        } catch(err) {
            console.error(err)
            res.send('Image does not exist')
            log_api_error('/:folder/:storm/:archive/:imageType/:imageFile',err)
            next()
        }
    });

    //route to submit tags of an image and get next image.
    router.post('/submit_image_tags', async function (req, res) {
        log_api('/submit_image_tags')
        res.setHeader('Access-Control-Allow-Origin', '*');
        try {
            const {
                developmentGroup,
                washoverVisibilityGroup,
                impactGroup,
                terrianGroup,
                additional_notes,
                image_id,
                user_id,
                user_name,
                time_end_tagging,
                time_start_tagging
            } = req.body

            log_img(image_id,user_name,user_id) 
            log(`Tagging time for submit ${chalk.yellow(time_end_tagging-time_start_tagging)} ms`)
            //console.log(developmentGroup,washoverVisibilityGroup,impactGroup)
            if(user_id && developmentGroup && washoverVisibilityGroup && impactGroup && terrianGroup && image_id) {
                //Now to check the passed in data.
                const devGroupCheck=[developmentGroup].every(val => possible_developmentGroup_tags.includes(val))
                const washoverCheck=[washoverVisibilityGroup].every(val => possible_washoverVisibilityGroup_tags.includes(val))
                const impactCheck=[impactGroup].every(val => possible_impactGroup_tags.includes(val))

                //console.log(!devGroupCheck,!washoverCheck,!impactCheck)
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

                //[ 'NodeId', 'SandyCoastlineId', 'MarshId', 'RiverId' ]

                const terrian_array= terrianGroup.includes('NodeId')? ['NodeId'] : terrianGroup

                //console.log(terrian_array)

                const terrian_tag_names_adjusted = terrian_array.map(element => {
                    return `terrian_${terrian_id_tag_pair[element]}`
                })

                //console.log(terrian_tag_names_adjusted)

                let json_terrian_array=[];

                terrian_tag_names_adjusted.forEach(element => {
                    json_terrian_array.push( {
                        "command": "tag",
                        "tag_operation": "add",
                        "tag": element,
                        "content": true
                    })
                })

                const json_args=gen_json_arg(user_id,[
                    {
                        "command": "tag",
                        "tag_operation": "add",
                        "tag": dev_cat,
                        "content": dev_value
                    },
                    {
                        "command": "tag",
                        "tag_operation": "add",
                        "tag": washover_cat,
                        "content": wash_value
                    },
                    {
                        "command": "tag",
                        "tag_operation": "add",
                        "tag": impact_cat,
                        "content": impact_value
                    },
                    {
                        "command": "tag",
                        "tag_operation": "add_notes",
                        "content": additional_notes
                    },
                    ...json_terrian_array,
                    {
                        "command": "tag",
                        "tag_operation": "next"
                    }
                ])
                log(chalk.yellow('Generated JSON arguments'))
                let options = {
                    mode: 'text',
                    pythonOptions: ['-u'],
                    scriptPath: './',
                    args: [
                        JSON.stringify(json_args)
                    ]
                };

                await runPy(`${assignerSrc}${assignerScript}`,function(err,results){
                    log(chalk.green('All tags added,and got next image'))
                },options)

                //Return
                res.send({
                    message:`Image has been tagged, page will refresh to get next image `
                })
                log_api_done(`/submit_image_tags`)

            }
            else
            {
                throw 'Not all tagging data was sent'
            }

        }catch (err){// big error
            //console.error(err);
            res.send({
                message:`ERROR - ${err}`
            })
            log_api_error('/submit_image_tags',err)
        }
    })

    //What to do for the quick option of saying this image is a ocean
    router.post('/submit_ocean_image', async function (req, res) {
        log_api('/submit_ocean_image')
        res.setHeader('Access-Control-Allow-Origin', '*');
        try {
            const {
                image_id,
                user_id,
                user_name,
                time_end_tagging,
                time_start_tagging
            } = req.body

            if(user_id && image_id) {
                log_img(image_id,user_name,user_id) 
                log(`Tagging time for ocean ${chalk.yellow(time_end_tagging-time_start_tagging)} ms`)
                const json_args=gen_json_arg(user_id,[
                    {
                        "command": "tag",
                        "tag_operation": "add",
                        "tag": "ocean",
                        "content": true
                    },
                    {
                        "command": "tag",
                        "tag_operation": "next"
                    }
                ])

                let options = {
                    mode: 'text',
                    pythonOptions: ['-u'],
                    scriptPath: './',
                    args: [
                        JSON.stringify(json_args)
                    ]
                };

                await runPy(`${assignerSrc}${assignerScript}`,function(err,results){
                    log('tagged as ocean and got next')
                    res.send({
                        message: `Image has been tagged as ocean, page will refresh to get new image`
                    })
                    log_api_done(`/submit_ocean_image`)
                },options)
            }
            else
            {
                throw 'Image ID not sent'
            }

        }catch (err){// big error
            //console.error(err);
            res.send({
                message:`ERROR - ${err}`
            })
            log_api_error('/submit_ocean_image',err)
        }
    })

    //skip image quick option
    router.post('/skip_image', async function (req, res) {
        log_api('/skip_image')
        try {
            res.setHeader('Access-Control-Allow-Origin', '*');
            const {
                user_id,
                image_id,
                user_name,
                time_end_tagging,
                time_start_tagging
            }=req.body;
            if(user_id && image_id) {
                log_img(image_id,user_name,user_id) 
                log(`Tagging time for skip ${chalk.yellow(time_end_tagging-time_start_tagging)} ms`)
                // Options to get the user's current image
                const json_args=gen_json_arg(user_id,[
                    {
                    "command": "tag",
                    "tag_operation": "skip"
                    }
                ])


                let options = {
                    mode: 'text',
                    pythonOptions: ['-u'],
                    scriptPath: './',
                    args: [
                        JSON.stringify(json_args)

                    ]
                };



                await runPy(`${assignerSrc}${assignerScript}`,function(err,results){
                    log('Image skipped')
                    res.send({
                        message: `Image skipped,page will refresh to get new image.`
                    })
                    log_api_done(`/skip_image`)
                },options)
            }
            else {
                throw 'Incomplete data sent'
            }
        } catch (err){// big error
            //console.error(err);
            res.send({
                message:`ERROR - ${err}`
            })
            log_api_error('/skip_image',err)
        }
    });
}
main();

//used below becuase https://stackoverflow.com/questions/27465850/typeerror-router-use-requires-middleware-function-but-got-a-object
module.exports = router ;
