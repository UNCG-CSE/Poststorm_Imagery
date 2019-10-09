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

import Button from '@material-ui/core/Button';
const useStyles = makeStyles(theme => ({
  button: {
    margin: theme.spacing(1),
  },
  input: {
    display: 'none',
  },
}));

export default function Index(props) {
  const classes = useStyles();
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
      <Grid
          container
          direction="column"
          justify="center"
          alignItems="center"
      >
        <Card className={classes.card}>
          <CardContent>
            <Typography variant="h5" component="h2" className={classes.title} color="textSecondary" gutterBottom>
              Welcome to Post Storm Image Classification Tagging Dashboard
            </Typography>

            <Typography className={classes.title} color="textSecondary" gutterBottom>       
              <Link href="/login"> 
                <Button >
                Please Login to continue
                </Button>
              </Link>
            </Typography>

          </CardContent>
         
        </Card>
      </Grid>
     
    </div>
  );
}