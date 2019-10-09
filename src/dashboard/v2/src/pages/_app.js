import React from 'react';
import App from 'next/app';
import Head from 'next/head';
import { ThemeProvider } from '@material-ui/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import theme from '../components/theme';
import Layout from '../components/Layout';
import {routePageNames} from '../components/routeToPageName';

export default class MyApp extends App {
  static async getInitialProps({ Component, ctx }) {
    let pageProps = {};
    if (Component.getInitialProps) {
      pageProps = await Component.getInitialProps(ctx);
    }
    if (ctx.req && ctx.req.session.passport) {
      pageProps.user = ctx.req.session.passport.user;
    }
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
    console.log(pageName)
    return (
      <React.Fragment>
        <Head>
          <title>{pageName}</title>
        </Head>
        <ThemeProvider theme={theme}>
          {/* CssBaseline kickstart an elegant, consistent, and simple baseline to build upon. */}
          <CssBaseline />
          <Layout user={this.state.user} pageName={pageName}>
          <Component {...pageProps} />
          </Layout>
          
        </ThemeProvider>
      </React.Fragment>
    );
  }
}
