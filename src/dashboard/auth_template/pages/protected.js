import React, { useState } from 'react';
import MyTheme from '../src/theme';
import Link from 'next/link'
import Button from '@material-ui/core/Button';

import TextField from '@material-ui/core/TextField';

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
  const [values, setValues] = React.useState({
    name: 'a',
    password: 'a'
   
  });

  const handleChange = name => event => {
    setValues({ ...values, [name]: event.target.value });
  };

  function handleSubmit(event){
    event.preventDefault();
      console.log(values)
  }
  return (
   <div>
     <h1>
       PROTECTED PAGE :)
     </h1>
     <Link href="/login">
        <Button color="primary" className={classes.button}>
            Login
        </Button>   
    </Link>
   </div>
  );
}