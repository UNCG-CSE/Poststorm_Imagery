import React from 'react';
import App from 'next/app';
import Head from 'next/head';
import { ThemeProvider } from '@material-ui/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import theme from '../components/theme';
import Layout from '../components/Layout/Layout';
import {routePageNames} from '../components/routeToPageName';

const axios = require('axios');

const serverConfig =require('../server-config')


export default class MyApp extends App {
  static async getInitialProps({ Component, ctx }) {
    const IP=await serverConfig.getIp()
    const BEARER= ''//await auth0Token.getAuth0Token()
   
    
    let pageProps = {};
    if (Component.getInitialProps) {
      pageProps = await Component.getInitialProps(ctx);
    }

    if (ctx.req && ctx.req.session.passport) {
      pageProps.user = ctx.req.session.passport.user;

      //This is so that it will only add the role if the user prop actualy exists
      if(pageProps.user) {
        var getUserOptions = {
          url: `http://${IP}:3000/api/getUserRole/${pageProps.user.user_id}`,
        };
        console.log(getUserOptions.url)
        const userRole=await axios.get(getUserOptions.url, getUserOptions)
        .then(function (response) {
         return response.data
        })
        pageProps.user.userRole=userRole
      } 
    }
    pageProps.ip=IP
    return { pageProps };
  }

  constructor(props) {
    super(props);
    this.state = {
      user: props.pageProps.user,
      pageName:'APP'
    };
  }

  componentDidMount() {
    // Remove the server-side injected CSS.
    const jssStyles = document.querySelector('#jss-server-side');
    if (jssStyles) {
      jssStyles.parentNode.removeChild(jssStyles);
    }
  }



  render() {
    const { Component, pageProps,router } = this.props;
    const {route}= router
    const props = {
      ...pageProps,
      user: this.state.user,
    };

  
    const pageInfo=routePageNames.filter(
      function(element){ return element.route == route }
    )[0]

    const pageName = pageInfo===undefined ? 'Welcome Page':pageInfo.name
   
    return (
      <React.Fragment>
        <Head>
          <title>{pageName}</title>
        </Head>
        <ThemeProvider theme={theme}>
          {/* CssBaseline kickstart an elegant, consistent, and simple baseline to build upon. */}
          <CssBaseline />
          <Layout user={this.state.user} pageName={pageName} >
            
          <Component user={this.state.user} {...pageProps} ip={props.ip}/>
      
          </Layout>
          
        </ThemeProvider>
      </React.Fragment>
    );
  }
}
