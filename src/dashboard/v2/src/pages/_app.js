import React from 'react';
import App from 'next/app';
import Head from 'next/head';
import { ThemeProvider } from '@material-ui/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import theme from '../components/theme';
import Layout from '../components/Layout/Layout';
import routePageNames from '../components/routeToPageName';

//Used to do POST/GET requests
const axios = require('axios');
//Contains what IP we using
const serverConfig =require('../server-config')


export default class MyApp extends App {
  static async getInitialProps({ Component, ctx }) {
    const IP=await serverConfig.getIp()
    
    let pageProps = {};
    //Get inital props
    if (Component.getInitialProps) {
      pageProps = await Component.getInitialProps(ctx);
    }

    //If theres a session from passport, add the user
    if(ctx.req.session){
      if (ctx.req && ctx.req.session.passport) {
        pageProps.user = ctx.req.session.passport.user;
  
        //This is so that it will only add the role if the user prop actualy exists
        if(pageProps.user) {
  
          //Lets get the userrole,by calling our own api that needs the user ID
          var getUserOptions = {
            url: `http://${IP}:3000/api/getUserRole/${pageProps.user.user_id}`,
          };
  
          pageProps.user.userRole=await axios.get(getUserOptions.url, getUserOptions)
          .then(function (response) {
           return response.data
          })
        } 
      }
    }
   

    //lets tag on the IP onto the pageProps
    pageProps.ip=IP
    return { pageProps };
  }

  constructor(props) {
    super(props);
    this.state = {
      user: props.pageProps.user,
      pageName:'APP NAME'
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
    //extract from props
    const { Component, pageProps,router } = this.props;
    //used to get page title
    const {route}= router
    const props = {
      ...pageProps,
      //user: this.state.user,
    };

    const pageName = routePageNames.getPageTitle(route);
   
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
