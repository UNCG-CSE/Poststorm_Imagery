import React, { useState } from 'react';
import MyTheme from '../src/theme';
import Link from 'next/link'
import Button from '@material-ui/core/Button';

import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(theme => ({
  button: {
    margin: theme.spacing(1),
  },  
  headerLabel:{
    color:MyTheme.palette.primary.main
  },
  container:{
    backgroundColor:'#444'
  }
}));

export default function Index() {
  const classes = useStyles();
  return (
   <div>
     <div>
       Home page
     </div>
     <Link href="/login">
        <Button color="primary" className={classes.button}>
          Login
        </Button>   
      </Link>
      <Link href="/register">
        <Button color="primary" className={classes.button}>
          Register
        </Button>   
      </Link>
      <Link href="/protected">
        <Button color="primary" className={classes.button}>
          Protected
        </Button>   
      </Link>
      <Link href="/unprotected">
        <Button color="primary" className={classes.button}>
          Unprotected
        </Button>   
      </Link>

   </div>
  );
}