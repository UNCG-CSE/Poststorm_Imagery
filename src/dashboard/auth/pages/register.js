import React, { useState } from 'react';
import Layout from '../src/components/layouts/layout'
import LoginRegisterLayout from '../src/components/layouts/loginRegisterLayout'
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(theme => ({

}));

export default function Index() {
  return (
    <Layout>  
      <LoginRegisterLayout type='register'/>   
    </Layout>
  );
}