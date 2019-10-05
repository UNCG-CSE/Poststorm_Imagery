import React, { useState } from 'react';
import MyTheme from '../src/theme';
import Button from '@material-ui/core/Button';
import { makeStyles } from '@material-ui/core/styles';
import Link from 'next/link'
//for fixing flex
import CssBaseline from '@material-ui/core/CssBaseline';
//testing for cetnered signi
import Container from '@material-ui/core/Container';
//for the title in login
import Typography from "@material-ui/core/Typography";
import TextField from '@material-ui/core/TextField';

import axios from 'axios';

const useStyles = makeStyles(theme => ({
  button: {
    margin: theme.spacing(1),
  },  
  headerLabel:{
    color:MyTheme.palette.primary.main
  },
  container:{
    backgroundColor:'#444'
  },
  textField: {
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
    width: 200,
  }
}));

export default function Index() {
  const classes = useStyles();
  const [values, setValues] = React.useState({
    username:'a',
    password:'a'
   
  });

  const handleChange = name => event => {
    setValues({ ...values, [name]: event.target.value });
  };

  function submitForm()
  {
    const form_values={
      username:values.username,
      password:values.password

    }
    axios.post(`http://localhost:3000/registerUser`, form_values)
    .then(res => {
      
      console.log(res.data);
    })    
  }
  return (

      <Container component="main" maxWidth="sm" className={classes.container}>

        <CssBaseline />
        <Typography component="h1" variant="h5" className={classes.headerLabel}>
          Register
        </Typography>
        <div>
        <form className={classes.container} noValidate autoComplete="off">
          <TextField
            id="standard-name"
            label="Name"
            className={classes.textField}
            value={values.username}
            onChange={handleChange('username')}
            margin="normal"
          />
          <TextField
            id="standard-name"
            label="Password"
            className={classes.textField}
            value={values.password}
            onChange={handleChange('password')}
            margin="normal"
          />
          <Button color="primary" className={classes.button} onClick={submitForm}>
            SUBMIT
          </Button>   
        </form>
        </div>
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
        <Link href="/login">
          <Button color="primary" className={classes.button}>
            Login
          </Button>   
        </Link>
        
      </Container>     
  
  );
}