import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Link from "next/link";
// import Link from "next/link";
// import Link from "../components/Link";

import Grid from '@material-ui/core/Grid';

import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import CenterGrid from '../../components/CenterGrid'


import Button from '@material-ui/core/Button';
const useStyles = makeStyles(theme => ({
  button: {
    margin: theme.spacing(1),
  },
  input: {
    display: 'none',
  },
  card: {
    minWidth: 275,
    width: '75%',
    display:'flex'
  },
}));

function dashboardHome(props) {
  const classes = useStyles();
  const hasUser=props.user !==undefined
  const max_stage=5;
  const [stage, setStage] = useState(0);
  
  function nextStage(){
    setStage((stage+1)%max_stage)
  }
  function prevStage(){
    const x =stage-1
    const n=max_stage
  
    setStage((x % n + n) % n)
  }

  return (
    <div> 
      <CenterGrid>
        <Card className={classes.card}>
          <CardContent>
            <Typography variant="h5" component="h2" className={classes.title} color="textSecondary" gutterBottom>
              Dashboard
            </Typography>

            <Typography color="textSecondary" gutterBottom>
              Welcome to Image Tagger {JSON.stringify(props.initProps)}
            </Typography>
            { Object.keys(props.user).map(key => (
              <li key={key}>{key}: {props.user[key].toString()}</li>
            ))}
           
            Role:{props.user.userRole.data[0].name}
            
          </CardContent>
          
        </Card>
      </CenterGrid>
     
    </div>
  );
}

dashboardHome.getInitialProps = async function(props) {
  //console.log(props)
  return {
    initProps:props.query
  }
}


export default dashboardHome;