import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';


import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import CenterGrid from '../components/CenterGrid'

import Button from '@material-ui/core/Button';

//form validation
import { Formik, Field, Form } from "formik";
import * as Yup from 'yup'

//for dropdown select
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

const useStyles = makeStyles(theme => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  input: {
    display: 'none',
  },
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  },
}));

function Index(props) {
  const classes = useStyles();
  const hasUser=props.user !==undefined
  const [stormValue, setValues] = React.useState({
    stormId: 0
  });

  
  const handleChange = event => {
    
    setValues(oldValues => ({
      stormId:event.target.value
    }));

  };

  const handleSubmit = () => {
    // axios.post(`http://34.74.4.64:4000/form_submit`, form_values)
    // .then(res => {
    //   console.log(res);
    //   console.log(res.data);
    // })
  }
  


  return (
    <div> 
      <CenterGrid>
        <Card className={classes.card}>
          <CardContent>
            <Typography variant="h5" component="h2" className={classes.title} color="textSecondary" gutterBottom>
              Please select a storm to start tagging on.
            </Typography>
            
            <form onSubmit={handleSubmit}>
              <FormControl variant="filled" className={classes.formControl} fullWidth>
                <InputLabel htmlFor="filled-age-simple">Storm</InputLabel>
                <Select
                  value={stormValue.stormId}
                  onChange={handleChange}
                  inputProps={{
                    name: 'storm',
                    id: 'idPickedStorm',
                  }}
                >
                  <MenuItem value={0}>Storm 1</MenuItem>
                  <MenuItem value={1}>Storm 2</MenuItem>
                  <MenuItem value={2}>Storm 3</MenuItem>
                </Select>
              </FormControl>
          
              <Button id="submitButtie" size="small" variant="contained" color="primary" className={classes.toolbarButtons} type="submit">
                  Submit
              </Button>
            </form>
            

          </CardContent>
         
        </Card>
      </CenterGrid>
     
    </div>
  );
}

Index.getInitialProps = async function() {
  return {
    initProps:'initPropValue'
  }
}


export default Index;