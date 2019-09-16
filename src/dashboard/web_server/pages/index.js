import Layout from "../components/layout";
import MyTheme from "../src/theme";
import React from "react";
import PropTypes from "prop-types";
import { createMuiTheme,makeStyles, useTheme, withStyles  } from "@material-ui/core/styles";
import { red, purple } from '@material-ui/core/colors';
import { ThemeProvider } from '@material-ui/styles';
import Fetch from 'isomorphic-unfetch';



import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Button from '@material-ui/core/Button';
import Typography from "@material-ui/core/Typography";

import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';


import FormGroup from '@material-ui/core/FormGroup';
import Checkbox from '@material-ui/core/Checkbox';


import Grid from '@material-ui/core/Grid';

const drawerWidth = 240;
const SAD_FACE = `
https://www.nationwidechildrens.org/-/media/nch/giving/images/on-our-sleeves-1010/icons/icon-teasers/w45084_iconcollectionlandingiconteaserimages_facesad.jpg
`;

const ColorButton = withStyles(theme => ({
  root: {
    color: theme.palette.getContrastText(red[500]),
    backgroundColor: red[500],
    '&:hover': {
      backgroundColor: red[900],
    },
  },
}))(Button);

const useStyles = makeStyles(theme => ({
  formControl: {
    margin: theme.spacing(3),
  },
  root_grid: {
    display: "flex",
    flexWrap: "wrap",
    justifyContent: "space-around",
    overflow: "hidden",
    backgroundColor: theme.palette.background.paper
  },
  root: {
    display: "flex"
  },
  drawer: {
    [theme.breakpoints.up("sm")]: {
      width: drawerWidth,
      flexShrink: 0
    }
  },
  appBar: {
    marginLeft: drawerWidth,
    [theme.breakpoints.up("sm")]: {
      width: `calc(100% - ${drawerWidth}px)`
    }
  },
  menuButton: {
    marginRight: theme.spacing(2),
    [theme.breakpoints.up("sm")]: {
      display: "none"
    }
  },
  toolbar: theme.mixins.toolbar,
  drawerPaper: {
    width: drawerWidth
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing(3)
  },
  paper: {
    padding: theme.spacing(3, 0),
    margin: theme.spacing(0, 0)
  },
  gridList: {
    width: 500,
    height: 450
  },
  icon: {
    color: "rgba(255, 255, 255, 0.54)"
  },
  card: {
    maxWidth: 700
  },
  
  media: {
    display:'fluid'
  }
}));

function Index(props) {
  const classes = useStyles();

  const [devTypeValue, setDevTypeValue] = React.useState('');
  const [washoverValue, setWashoverValue] = React.useState('');
  const [IDKVALUE, setIDKVALUE] = React.useState('');

  function handleChange(fnc,event) {
    fnc(event.target.value);
  }
  
  //check boxes
  const [checkbox_state, setState_checkbox] = React.useState({
    Marsh: false,
    River: false,
    SandyCoastline: false,
  });

  const handleChange_checkbox = name => event => {
    setState_checkbox({ ...checkbox_state, [name]: event.target.checked });
  };

  const { Marsh, River, SandyCoastline } = checkbox_state;
  

  return (
    <Layout>
    <Grid
        container
        direction="row"
        justify="center"
        alignItems="center"
      >
      <Card className={classes.card}>
        <CardActionArea>
          <CardMedia
            component="img"
            alt="Contemplative Reptile"
            height="fluid"
            image={props.data.url || SAD_FACE}
            title="Contemplative Reptile"
          />
          <CardContent>
            <Typography gutterBottom variant="h5" component="h2">
              {props.data.file_name}
            </Typography>
            <Typography variant="body2" color="textSecondary" component="p">
            {JSON.stringify(props.data, null, 4)}
            </Typography>
            
          </CardContent>
        </CardActionArea>

        <FormControl component="fieldset" className={classes.formControl}>
          <FormLabel component="legend" style={MyTheme.palette.amber500}>Development type</FormLabel>
          <RadioGroup aria-label="DevType" name="DevType" value={devTypeValue} onChange={(e) => handleChange(setDevTypeValue, e)} row>
            <FormControlLabel  value="Developed" control={<Radio style={MyTheme.palette.amber500} />} label="Developed"  />
            <FormControlLabel  value="Undevelopd" control={<Radio style={MyTheme.palette.amber500} />} label="Undevelopd" />
          </RadioGroup>
        </FormControl>

        <br/>

        <FormControl component="fieldset" className={classes.formControl}>
          <FormLabel component="legend" style={MyTheme.palette.purple500}>Land Type</FormLabel>
          <FormGroup row>
            <FormControlLabel
              control={<Checkbox checked={River} onChange={handleChange_checkbox('River')} value="River" style={MyTheme.palette.purple500}/>}
              label="River" 
            />
            <FormControlLabel
              control={<Checkbox checked={Marsh} onChange={handleChange_checkbox('Marsh')} value="Marsh" style={MyTheme.palette.purple500}/>}
              label="Marsh" 
            />
            <FormControlLabel
              control={
                <Checkbox checked={SandyCoastline} onChange={handleChange_checkbox('SandyCoastline')} value="Sandy Coastline" style={MyTheme.palette.purple500}/>
              }
              label="Sandy Coastline" 
            />
          </FormGroup>
        </FormControl>
        
        <br/>

        <FormControl component="fieldset" className={classes.formControl}>
          <FormLabel component="legend" style={MyTheme.palette.blue500}>Washover type</FormLabel>
          <RadioGroup aria-label="WashoverType" name="WashoverType" value={washoverValue} onChange={(e) => handleChange(setWashoverValue, e)} row>
            <FormControlLabel value="Visable Washover" control={<Radio style={MyTheme.palette.blue500} />} label="Visable Washover"  />
            <FormControlLabel value="No Visable Washover" control={<Radio style={MyTheme.palette.blue500} />} label="No Visable Washover" />
          </RadioGroup>
        </FormControl>

        <br/>

        <FormControl component="fieldset" className={classes.formControl}>
          <FormLabel component="legend" style={MyTheme.palette.green500}>IDK WHAT TO CALL THIS</FormLabel>
          <RadioGroup aria-label="IDKWATTHISIS" name="IDKWATTHISIS" value={IDKVALUE} onChange={(e) => handleChange(setIDKVALUE, e)} row>
            <FormControlLabel value="Swash" control={<Radio style={MyTheme.palette.green500} />} label="Swash"  />
            <FormControlLabel value="Collision" control={<Radio style={MyTheme.palette.green500} />} label="Collision" />
            <FormControlLabel value="Inundation" control={<Radio style={MyTheme.palette.green500} />} label="Inundation"  />
            <FormControlLabel value="Overwash" control={<Radio style={MyTheme.palette.green500} />} label="Overwash" />
          </RadioGroup>
        </FormControl>

        <CardActions style={MyTheme.palette.cyan800BG}>
          {/* <Button size="small" variant="contained" color="inherit" style={MyTheme.palette.red500}>
            Skip
          </Button> */}
       
          <ColorButton size="small" variant="contained" color="primary" className={classes.margin}>
            Skip
          </ColorButton>
          <ColorButton right size="small" variant="contained" color="primary" className={classes.margin}>
            Submit
          </ColorButton>
        </CardActions>
      </Card>
      </Grid>
    </Layout>
  );
}

Index.propTypes = {
  /**
   * Injected by the documentation to work in an iframe.
   * You won't need it on your project.
   */
  container: PropTypes.instanceOf(
    typeof Element === "undefined" ? Object : Element
  )
};

Index.getInitialProps = async function() {
  //first get constants
  const CONSTANTS = await require('../server_constants')
  const {SITE_IP} = CONSTANTS
  
  //This enables it so that the serve either uses localhost or the machines ip,all based off if the user gives a cl arg.
  const API_URL=`http://${SITE_IP.node}/images/get_image`
  //Default data incase Fetch fails. 
  let data,default_data = {
      file_url:undefined,
      file_name:'ERROR API CALL FAILED',
      file_desc: 'BIG SAD',
      api_url:API_URL,
  }
  
  //Now we call the get image api to ,well get the image
  await fetch(API_URL).then(async function(received_data) { 
      data = await received_data.json()
      
  }).catch(function() {
      
  });

  return {
      data:data || default_data
  }

}

export default Index;
