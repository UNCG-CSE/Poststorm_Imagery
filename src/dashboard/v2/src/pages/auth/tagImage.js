import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';


import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import CenterGrid from '../../components/CenterGrid'

import Button from '@material-ui/core/Button';

//form validation
import { Formik, Form, Field } from "formik";
import { TextField } from "material-ui-formik-components/TextField";
import { Select } from "material-ui-formik-components/Select";
import * as Yup from 'yup'

//tab
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Box from '@material-ui/core/Box';

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <Typography
      component="div"
      role="tabpanel"
      hidden={value !== index}
      id={`wrapped-tabpanel-${index}`}
      aria-labelledby={`wrapped-tab-${index}`}
      {...other}
    >
      <Box p={3}>{children}</Box>
    </Typography>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.any.isRequired,
  value: PropTypes.any.isRequired,
};

function a11yProps(index) {
  return {
    id: `wrapped-tab-${index}`,
    'aria-controls': `wrapped-tabpanel-${index}`,
  };
}

const useStyles = makeStyles(theme => ({
  root: {
    // display: 'flex',
    // flexWrap: 'wrap',
    backgroundColor: theme.palette.background.paper,
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
  
  const [value, setValue] = React.useState('one');

  const handleChange = ( newValue) => {
    setValue(newValue);
  };


  return (
    <div> 
      <CenterGrid>
        <div className={classes.root}>
          <AppBar position="static">
            <Tabs value={value}  aria-label="wrapped label tabs example">
              <Tab
                value="one"
                label="Select a Storm"
                wrapped
                {...a11yProps('one')}
              />
              <Tab value="two" label="Tag an image" {...a11yProps('two')} />
             
            </Tabs>
          </AppBar>
          <TabPanel value={value} index="one">
      
              <CardContent>
                <Typography variant="h5" component="h2" className={classes.title} color="textSecondary" gutterBottom>
                  Please select a storm to start tagging on.
                </Typography>
              
                <Formik
                  initialValues={{
                    stormId: -1
                  }}
                  validationSchema={Yup.object().shape({
                    stormId: Yup.number().positive().required("Please select a option"),
                    //additionalNotes: Yup.string(),
                  })}
                  onSubmit={values => {
                    //alert(`Gender: ${values.stormId}`);
                    handleChange('two')
                    // axios.post(`http://34.74.4.64:4000/form_submit`, form_values)
                    // .then(res => {
                    //   console.log(res);
                    //   console.log(res.data);
                    // })
                  }}
                  render={props => (
                    <Form>
                    
                      <Field
                        required
                        name="stormId"
                        label="Storm"
                        options={[
                          { value: 1, label: "Storm 1" },
                          { value: 2, label: "Storm 2" },
                          { value: 3, label: "Storm 3" }
                        ]}
                        component={Select}
                      />
                      {console.log(props.errors)}
                      <button
                        type="submit"
                        disabled={props.values.stormId==-1}
                      >
                        Submit
                      </button>
                    </Form>
                  )}
                />
              </CardContent>
          </TabPanel>
          <TabPanel value={value} index="two">
            Item Two
          </TabPanel>
        </div>
        
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