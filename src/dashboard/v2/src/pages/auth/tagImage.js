import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';


import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import CenterGrid from '../../components/CenterGrid'

import Button from '@material-ui/core/Button';

//form validation
import { Formik, Form, Field, ErrorMessage } from "formik";
import { TextField } from "material-ui-formik-components/TextField";
import { Select } from "material-ui-formik-components/Select";
import * as Yup from 'yup'

//tab
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Box from '@material-ui/core/Box';

import MyTheme from '../../components/theme';
const axios = require('axios');
import fetch from 'isomorphic-unfetch';


import DisplayImage from '../../components/image_tagging/displayImage';

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <Typography
      component="div"
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
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
    flexGrow: 1,
    backgroundColor: theme.palette.background.paper,
  },
}));

function Index(props) {
  const classes = useStyles();
  const hasUser=props.user !==undefined
  const IP=props.ip
  const [value, setValue] = React.useState(0);

  const handleChange = (newValue) => {
    setValue(newValue);
  };

  return (
    <div> 
      <CenterGrid>
        <div className={classes.root}>
          <AppBar position="static">
            <Tabs value={value} onChange={handleChange} aria-label="simple tabs example">
              <Tab label="Pick a storm" {...a11yProps(0)} />
              <Tab label="Tag Image" {...a11yProps(1)} disabled/>
             
            </Tabs>
          </AppBar>
          <TabPanel value={value} index={0}>
            <Formik
                initialValues={{
                  stormId: -1
                }}
                validationSchema={Yup.object().shape({
                  stormId: Yup.number().positive('Please select a option').required("Please select a option"),
                })}
                onSubmit={async (values )=> {
                  console.log(values,IP)
                  // const response = await fetch(`http://${IP}:3000/api/stormToTag`, {
                  //   method: 'POST', // *GET, POST, PUT, DELETE, etc.
                  //   mode: 'cors', // no-cors, *cors, same-origin
                  //   cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
                  //   credentials: 'same-origin', // include, *same-origin, omit
                  //   headers: {
                  //     'Content-Type': 'application/json'
                  //     // 'Content-Type': 'application/x-www-form-urlencoded',
                  //   },
                  //   redirect: 'follow', // manual, *follow, error
                  //   referrer: 'no-referrer', // no-referrer, *client
                  //   body: JSON.stringify(values) // body data type must match "Content-Type" header
                  // });
                  // await response.json(); 
                  handleChange(1)
                  axios.post(`http://${IP}:3000/api/stormToTag`, values)
                  .then(res => {
                    console.log(res);
                    console.log(res.data);
                  })
                }}
                render={propsFormik => (
                  <Form>
                  
                    <Field
                      required
                      name="stormId"
                      label="Storm"
                      options={[
                        ...props.initProps.storms
                      ]}
                      component={Select}
                      error={propsFormik.errors.stormId !== undefined}
                    />
                    { propsFormik.errors.stormId &&
                      (<div style={MyTheme.palette.red500}>
                        {propsFormik.errors.stormId}
                      </div>)
                    }
                    {/* <button
                      type="submit"
                      disabled={propsFormik.values.stormId==-1}
                    >
                      Submit
                    </button> */}

                    <Button 
                    variant="contained"
                    type="submit"
                    color="primary"
                    disabled={propsFormik.values.stormId==-1}
                    >
                      Default
                    </Button>
                    
                  </Form>
                )}
              />
          </TabPanel>
          <TabPanel value={value} index={1} >
            <DisplayImage/>
          </TabPanel>
        </div>
      </CenterGrid>
     
    </div>
  );
}

Index.getInitialProps = async function(props) {
  const serverConfig =require('../../server-config')
  const IP=await serverConfig.getIp()
  
  let fetchPayload = [
    {label:"Storm #1",value:1},
    {label:"Storm Dos",value:420},
    {label: "Storm III",value:1337}
  ]
  
  try {
    const response = await fetch(`http://${IP}:3000/api/getTaggableStorms`);
    fetchPayload = (await response.json()).storms;
  } catch (err) {
    console.log('error API failed to get storms')
  }
  
  return {
    initProps:{
      storms:fetchPayload
    }
  }
  
}


export default Index;