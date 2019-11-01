import React, {useState} from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Link from '../components/Link' //"next/link";
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import CenterGrid from '../components/CenterGrid'

import Button from '@material-ui/core/Button';

const useStyles = makeStyles(theme => ({
  button: {
    margin: theme.spacing(1),
  },
  input: {
    display: 'none',
  },
}));

function Index(props) {
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

  function showShouldLogin(){
    if(!hasUser){
      return (
        <Typography className={classes.title} color="textSecondary" gutterBottom>
          <Link href="/login">
            <Button color="primary" variant="outlined">
            Please Login to continue
            </Button>
          </Link>
        </Typography>
      )
    }
    else {
      return (
        <Typography className={classes.title} color="textSecondary" gutterBottom>
          <Link href="/auth/tagImage">
            <Button color="primary" variant="outlined">
            Please go and tag an image :) :)
            </Button>
          </Link>
        </Typography>
      )
    }
  }

  return (
    <div>
      <CenterGrid>
        <Card className={classes.card}>
          <CardContent>
            <Typography variant="h5" component="h2" className={classes.title} color="textSecondary" gutterBottom>
              Welcome to Post Storm Image Classification Tagging Dashboard

            </Typography>
            {showShouldLogin()}
          </CardContent>
        </Card>
      </CenterGrid>

    </div>
  );
}

Index.getInitialProps = async function() {
  const serverConfig =require('../server-config')

  return {
    initProps:{
      IP:await serverConfig.getIp()
    }
  }
}


export default Index;
