import Layout from "../components/layout";
import MyTheme from "../src/theme";
import React from "react";
import PropTypes from "prop-types";
import { makeStyles, useTheme } from "@material-ui/core/styles";
import Fetch from 'isomorphic-unfetch';

import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Button from '@material-ui/core/Button';
import Typography from "@material-ui/core/Typography";

import Grid from '@material-ui/core/Grid';

const drawerWidth = 240;
const SAD_FACE = `
https://www.nationwidechildrens.org/-/media/nch/giving/images/on-our-sleeves-1010/icons/icon-teasers/w45084_iconcollectionlandingiconteaserimages_facesad.jpg
`;

const useStyles = makeStyles(theme => ({
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
    maxWidth: 700,
    maxHeight:700
  },
  
  media: {
    display:'fluid'
  },
}));

function Index(props) {
  const classes = useStyles();
  const [expanded, setExpanded] = React.useState(false);
  function handleExpandClick() {
    setExpanded(!expanded);
  }

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
        <CardActions style={MyTheme.palette.blue400BG}>
          <Button size="small" color="primary" style={MyTheme.palette.amber500}>
            Skip
          </Button>
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
