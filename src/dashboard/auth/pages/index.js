import React, { useState } from 'react';
import MyTheme from '../src/theme';
import Layout from '../src/components/layouts/layout'
import Button from '@material-ui/core/Button';
import { makeStyles } from '@material-ui/core/styles';
import Link from 'next/link'

//for fixing flex
import CssBaseline from '@material-ui/core/CssBaseline';

//testing for cetnered signi
import Container from '@material-ui/core/Container';

//for the title in login
import Typography from "@material-ui/core/Typography";

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
    <Layout>  
      
      <Container component="main" maxWidth="sm" className={classes.container}>

        <CssBaseline />
        <Typography component="h1" variant="h5" className={classes.headerLabel}>
          Welcome to Post Storm Image Tagger
        </Typography>
        <Link href="/login">
          <Button color="primary" className={classes.button}>
            Login?
          </Button>   
        </Link>
        <Link href="/register">
          <Button color="primary" className={classes.button}>
            Register?
          </Button>   
        </Link>
        
      </Container>     
    </Layout>
  );
}