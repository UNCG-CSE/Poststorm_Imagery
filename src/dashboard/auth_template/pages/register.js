import React, { useState } from 'react';
import MyTheme from '../src/theme';
import Link from 'next/link'
import Button from '@material-ui/core/Button';

import TextField from '@material-ui/core/TextField';

import { makeStyles } from '@material-ui/core/styles';
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
    axios.post(`http://localhost:3000/createUser`, values)
        .then(res => {
          console.log(res)
        //alert(res.data)
        //Router.push('/api/protec')
    }).catch(res =>{
      //Router.push('/register')
    })
  }
  return (
   <div>
     <div>
       Register
     </div>
    <form className={classes.container} noValidate autoComplete="off" onSubmit={handleSubmit}>
        <div>
            <TextField
                id="standard-name"
                label="Name"
                className={classes.textField}
                value={values.name}
                onChange={handleChange('name')}
                margin="normal"
            />
        </div>

        <div>
            <TextField
                id="standard-name"
                label="Password"
                className={classes.textField}
                value={values.password}
                onChange={handleChange('name')}
                margin="normal"
            />
        </div>

        <Button type="submit" color="primary" className={classes.button}>
            submit
        </Button>   
       
    </form>
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
   </div>
  );
}