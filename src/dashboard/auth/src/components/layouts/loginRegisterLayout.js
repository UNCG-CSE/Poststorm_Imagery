import React, { useState } from 'react';
import MyTheme from '../../theme';
import LoginFormik from '../forms/loginForm'
import RegisterFormik from '../forms/registerForm'

import { makeStyles } from '@material-ui/core/styles';

//for the title in login
import Typography from "@material-ui/core/Typography";

//for fixing flex
import CssBaseline from '@material-ui/core/CssBaseline';

//testing for cetnered signi
import Container from '@material-ui/core/Container';

//Our styles for the page
const useStyles = makeStyles(theme => ({
  link:{
    textDecoration:'none'
  },
  button: {
    margin: theme.spacing(1),
  },
  input: {
    display: 'none',
  },
  form: {
    //width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  button: {
    margin: theme.spacing(1),
  },
  headerLabel:{
    color:MyTheme.palette.primary.main
  }
}));

//This is stuff for register form
function registerGroup(classes){
  return (
    <>
      <Typography component="h1" variant="h5" className={classes.headerLabel}>
            Register
      </Typography>
      <RegisterFormik/>
    </>
  )
}

//stuff for the login page
function loginGroup(classes){
  return (
    <>
      <Typography component="h1" variant="h5" className={classes.headerLabel}>
        Sign in
      </Typography>
      <LoginFormik/>
    </>
  )
}

//Determine which form to use based of the prop
function determineFormType(type,classes){
  if(type==='login'){
    return (
      loginGroup(classes)
    )

  }
  if(type==='register'){
    return (
      registerGroup(classes)  
    )

  }
  return (
    <>
      ERROR NO TYPE SENT F
    </>  
    )
}

//main component
export default function loginRegisterLayout(props) {
    const classes = useStyles();
    return (
        <Container component="main" maxWidth="xs">
            <CssBaseline />
            <div > 
                {determineFormType(props.type,classes)}
            </div>
        </Container>     
    );
}
