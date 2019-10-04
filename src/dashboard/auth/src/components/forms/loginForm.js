import React, { useState } from 'react';
import MyTheme from '../../theme';

//Used to tie the error div in
import InputValidate from '../inputField'

import { makeStyles } from '@material-ui/core/styles';

import Link from 'next/link'

//buttons for login
import Button from '@material-ui/core/Button';

//used to align the login button right
//https://stackoverflow.com/questions/47686456/whats-the-right-way-to-float-right-or-left-using-the-material-ui-appbar-with-ma
import Grid from '@material-ui/core/Grid';

//for input validation
import { Formik } from 'formik';
import * as Yup from 'yup';

//Styles of our page
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

export default function loginRegisterLayout(props) {
  const classes = useStyles();
  return (
    <Formik 
      initialValues={{ 
          emailValue: '',
          passwordValue:'' 
      }}
      validationSchema={Yup.object().shape({
          emailValue: Yup.string().required("Please enter your email"),
          passwordValue: Yup.string().required("Please enter your password"),
      })}
      onSubmit={(values, actions) => {
          setTimeout(() => {
          alert(values.emailValue+'-'+values.passwordValue);
          actions.setSubmitting(false);
          }, 1000);
      }}
      render={props => (
        <form className={classes.form} onSubmit={props.handleSubmit} noValidate>
          <InputValidate
              variant="outlined"
              margin="normal"
              onChange={props.handleChange}
              onBlur={props.handleBlur}
              fullWidth
              id="emailId"
              label="Enter Email"
              name="emailValue"
              //autoComplete="email"
              
              errors={props.errors.emailValue}
              disabled={props.isSubmitting}
          />
          
          <InputValidate 
              variant="outlined"
              margin="normal"
              onChange={props.handleChange}
              onBlur={props.handleBlur}
              fullWidth
              name="passwordValue"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password" 
              disabled={props.isSubmitting}
              errors={props.errors.passwordValue} 
          
          />

          <Grid justify="space-between" container>
              <Grid item>
              <Link href="/register">
                  <Button   disabled={props.isSubmitting} color="secondary" className={classes.button} style={{ backgroundColor: 'transparent',textDecoration:'none' }}>
                  Register
                  </Button>
              </Link>
              </Grid>

              <Grid item>
                  <Button  disabled={props.isSubmitting} type="submit" variant="contained" color="primary" className={classes.button}>
                  Login
                  </Button>
              </Grid>
          </Grid>
        </form>
      )}
    />
  );
}
