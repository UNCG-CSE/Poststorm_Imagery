import React from 'react';
import App from 'next/app';
import Head from 'next/head';
import { ThemeProvider } from '@material-ui/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import theme from '../components/theme';
import Layout from '../components/Layout/Layout';
import {routePageNames} from '../components/routeToPageName';

const axios = require('axios');

export default class MyApp extends App {
  static async getInitialProps({ Component, ctx }) {

    

    //https://auth0.com/docs/users/search/v3/get-users-endpoint
    // var options = {
    //   method: 'GET',
    //   url: 'https://dev-testing-auth0.auth0.com/api/v2/users',
    //   qs: {q: 'email:"sarafiqu@uncg.edu"', search_engine: 'v3'},
    //   headers: {authorization: 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik9EQXpSVEV4TVRaQ1JqZ3lNVGc0TlRreE9VVTNOamREUlVFNE5UY3pSREUyTXprM05UUkJNZyJ9.eyJpc3MiOiJodHRwczovL2Rldi10ZXN0aW5nLWF1dGgwLmF1dGgwLmNvbS8iLCJzdWIiOiJWa2w4Q3g3WGdEM3pRWTB5dXNTcjVEYjJtZ2g1VVQ4dkBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9kZXYtdGVzdGluZy1hdXRoMC5hdXRoMC5jb20vYXBpL3YyLyIsImlhdCI6MTU3MDg0NzgyNywiZXhwIjoxNTcwOTM0MjI3LCJhenAiOiJWa2w4Q3g3WGdEM3pRWTB5dXNTcjVEYjJtZ2g1VVQ4diIsInNjb3BlIjoicmVhZDpjbGllbnRfZ3JhbnRzIGNyZWF0ZTpjbGllbnRfZ3JhbnRzIGRlbGV0ZTpjbGllbnRfZ3JhbnRzIHVwZGF0ZTpjbGllbnRfZ3JhbnRzIHJlYWQ6dXNlcnMgdXBkYXRlOnVzZXJzIGRlbGV0ZTp1c2VycyBjcmVhdGU6dXNlcnMgcmVhZDp1c2Vyc19hcHBfbWV0YWRhdGEgdXBkYXRlOnVzZXJzX2FwcF9tZXRhZGF0YSBkZWxldGU6dXNlcnNfYXBwX21ldGFkYXRhIGNyZWF0ZTp1c2Vyc19hcHBfbWV0YWRhdGEgY3JlYXRlOnVzZXJfdGlja2V0cyByZWFkOmNsaWVudHMgdXBkYXRlOmNsaWVudHMgZGVsZXRlOmNsaWVudHMgY3JlYXRlOmNsaWVudHMgcmVhZDpjbGllbnRfa2V5cyB1cGRhdGU6Y2xpZW50X2tleXMgZGVsZXRlOmNsaWVudF9rZXlzIGNyZWF0ZTpjbGllbnRfa2V5cyByZWFkOmNvbm5lY3Rpb25zIHVwZGF0ZTpjb25uZWN0aW9ucyBkZWxldGU6Y29ubmVjdGlvbnMgY3JlYXRlOmNvbm5lY3Rpb25zIHJlYWQ6cmVzb3VyY2Vfc2VydmVycyB1cGRhdGU6cmVzb3VyY2Vfc2VydmVycyBkZWxldGU6cmVzb3VyY2Vfc2VydmVycyBjcmVhdGU6cmVzb3VyY2Vfc2VydmVycyByZWFkOmRldmljZV9jcmVkZW50aWFscyB1cGRhdGU6ZGV2aWNlX2NyZWRlbnRpYWxzIGRlbGV0ZTpkZXZpY2VfY3JlZGVudGlhbHMgY3JlYXRlOmRldmljZV9jcmVkZW50aWFscyByZWFkOnJ1bGVzIHVwZGF0ZTpydWxlcyBkZWxldGU6cnVsZXMgY3JlYXRlOnJ1bGVzIHJlYWQ6cnVsZXNfY29uZmlncyB1cGRhdGU6cnVsZXNfY29uZmlncyBkZWxldGU6cnVsZXNfY29uZmlncyByZWFkOmVtYWlsX3Byb3ZpZGVyIHVwZGF0ZTplbWFpbF9wcm92aWRlciBkZWxldGU6ZW1haWxfcHJvdmlkZXIgY3JlYXRlOmVtYWlsX3Byb3ZpZGVyIGJsYWNrbGlzdDp0b2tlbnMgcmVhZDpzdGF0cyByZWFkOnRlbmFudF9zZXR0aW5ncyB1cGRhdGU6dGVuYW50X3NldHRpbmdzIHJlYWQ6bG9ncyByZWFkOnNoaWVsZHMgY3JlYXRlOnNoaWVsZHMgZGVsZXRlOnNoaWVsZHMgcmVhZDphbm9tYWx5X2Jsb2NrcyBkZWxldGU6YW5vbWFseV9ibG9ja3MgdXBkYXRlOnRyaWdnZXJzIHJlYWQ6dHJpZ2dlcnMgcmVhZDpncmFudHMgZGVsZXRlOmdyYW50cyByZWFkOmd1YXJkaWFuX2ZhY3RvcnMgdXBkYXRlOmd1YXJkaWFuX2ZhY3RvcnMgcmVhZDpndWFyZGlhbl9lbnJvbGxtZW50cyBkZWxldGU6Z3VhcmRpYW5fZW5yb2xsbWVudHMgY3JlYXRlOmd1YXJkaWFuX2Vucm9sbG1lbnRfdGlja2V0cyByZWFkOnVzZXJfaWRwX3Rva2VucyBjcmVhdGU6cGFzc3dvcmRzX2NoZWNraW5nX2pvYiBkZWxldGU6cGFzc3dvcmRzX2NoZWNraW5nX2pvYiByZWFkOmN1c3RvbV9kb21haW5zIGRlbGV0ZTpjdXN0b21fZG9tYWlucyBjcmVhdGU6Y3VzdG9tX2RvbWFpbnMgcmVhZDplbWFpbF90ZW1wbGF0ZXMgY3JlYXRlOmVtYWlsX3RlbXBsYXRlcyB1cGRhdGU6ZW1haWxfdGVtcGxhdGVzIHJlYWQ6bWZhX3BvbGljaWVzIHVwZGF0ZTptZmFfcG9saWNpZXMgcmVhZDpyb2xlcyBjcmVhdGU6cm9sZXMgZGVsZXRlOnJvbGVzIHVwZGF0ZTpyb2xlcyByZWFkOnByb21wdHMgdXBkYXRlOnByb21wdHMgcmVhZDpicmFuZGluZyB1cGRhdGU6YnJhbmRpbmciLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.HE1AJw69c4if0UbcZwrYiq6ttMPqBCa4BK0bNSW3SrQ4EWK-rcmWdYbWuz0uzDl6Lc9quvcMXAaDsALZws3o5XEBHdTwJsxJc_6hR3f9pjPlIEV1fELdXfJvkER6by6KPIsGMqWBixQdnWqy1no5Y7QhyqwzSJUOCcW7mN1JJpmA3l8U298_tsv5rrsXwNsk6Nkeco4TAScqKWfG7tpuW5L6klu7dZQwT9Tb8rOVcy_u5Ull29oAqVXBaEO6yosHu1SuLwCTGlX8TAYZbJYYH8g9MpW2jICqfa4sk4LAhj845PHV4IRe5yXLwU5Xdub2_sBp5_GeoTu8WDS8At4ikg'}
    // };
    
    // axios.get('https://dev-testing-auth0.auth0.com/api/v2/users', options)
    // .then(function (response) {
    //   //console.log((response.data));
    // })

    // var options2 = {
    //   method: 'GET',
    //   url: 'https://dev-testing-auth0.auth0.com/api/v2/users/google-oauth2|100613204270669384478/roles',
    //   qs: {q: 'email:"sarafiqu@uncg.edu"', search_engine: 'v3'},
    //   headers: {authorization: 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik9EQXpSVEV4TVRaQ1JqZ3lNVGc0TlRreE9VVTNOamREUlVFNE5UY3pSREUyTXprM05UUkJNZyJ9.eyJpc3MiOiJodHRwczovL2Rldi10ZXN0aW5nLWF1dGgwLmF1dGgwLmNvbS8iLCJzdWIiOiJWa2w4Q3g3WGdEM3pRWTB5dXNTcjVEYjJtZ2g1VVQ4dkBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9kZXYtdGVzdGluZy1hdXRoMC5hdXRoMC5jb20vYXBpL3YyLyIsImlhdCI6MTU3MDg0NzgyNywiZXhwIjoxNTcwOTM0MjI3LCJhenAiOiJWa2w4Q3g3WGdEM3pRWTB5dXNTcjVEYjJtZ2g1VVQ4diIsInNjb3BlIjoicmVhZDpjbGllbnRfZ3JhbnRzIGNyZWF0ZTpjbGllbnRfZ3JhbnRzIGRlbGV0ZTpjbGllbnRfZ3JhbnRzIHVwZGF0ZTpjbGllbnRfZ3JhbnRzIHJlYWQ6dXNlcnMgdXBkYXRlOnVzZXJzIGRlbGV0ZTp1c2VycyBjcmVhdGU6dXNlcnMgcmVhZDp1c2Vyc19hcHBfbWV0YWRhdGEgdXBkYXRlOnVzZXJzX2FwcF9tZXRhZGF0YSBkZWxldGU6dXNlcnNfYXBwX21ldGFkYXRhIGNyZWF0ZTp1c2Vyc19hcHBfbWV0YWRhdGEgY3JlYXRlOnVzZXJfdGlja2V0cyByZWFkOmNsaWVudHMgdXBkYXRlOmNsaWVudHMgZGVsZXRlOmNsaWVudHMgY3JlYXRlOmNsaWVudHMgcmVhZDpjbGllbnRfa2V5cyB1cGRhdGU6Y2xpZW50X2tleXMgZGVsZXRlOmNsaWVudF9rZXlzIGNyZWF0ZTpjbGllbnRfa2V5cyByZWFkOmNvbm5lY3Rpb25zIHVwZGF0ZTpjb25uZWN0aW9ucyBkZWxldGU6Y29ubmVjdGlvbnMgY3JlYXRlOmNvbm5lY3Rpb25zIHJlYWQ6cmVzb3VyY2Vfc2VydmVycyB1cGRhdGU6cmVzb3VyY2Vfc2VydmVycyBkZWxldGU6cmVzb3VyY2Vfc2VydmVycyBjcmVhdGU6cmVzb3VyY2Vfc2VydmVycyByZWFkOmRldmljZV9jcmVkZW50aWFscyB1cGRhdGU6ZGV2aWNlX2NyZWRlbnRpYWxzIGRlbGV0ZTpkZXZpY2VfY3JlZGVudGlhbHMgY3JlYXRlOmRldmljZV9jcmVkZW50aWFscyByZWFkOnJ1bGVzIHVwZGF0ZTpydWxlcyBkZWxldGU6cnVsZXMgY3JlYXRlOnJ1bGVzIHJlYWQ6cnVsZXNfY29uZmlncyB1cGRhdGU6cnVsZXNfY29uZmlncyBkZWxldGU6cnVsZXNfY29uZmlncyByZWFkOmVtYWlsX3Byb3ZpZGVyIHVwZGF0ZTplbWFpbF9wcm92aWRlciBkZWxldGU6ZW1haWxfcHJvdmlkZXIgY3JlYXRlOmVtYWlsX3Byb3ZpZGVyIGJsYWNrbGlzdDp0b2tlbnMgcmVhZDpzdGF0cyByZWFkOnRlbmFudF9zZXR0aW5ncyB1cGRhdGU6dGVuYW50X3NldHRpbmdzIHJlYWQ6bG9ncyByZWFkOnNoaWVsZHMgY3JlYXRlOnNoaWVsZHMgZGVsZXRlOnNoaWVsZHMgcmVhZDphbm9tYWx5X2Jsb2NrcyBkZWxldGU6YW5vbWFseV9ibG9ja3MgdXBkYXRlOnRyaWdnZXJzIHJlYWQ6dHJpZ2dlcnMgcmVhZDpncmFudHMgZGVsZXRlOmdyYW50cyByZWFkOmd1YXJkaWFuX2ZhY3RvcnMgdXBkYXRlOmd1YXJkaWFuX2ZhY3RvcnMgcmVhZDpndWFyZGlhbl9lbnJvbGxtZW50cyBkZWxldGU6Z3VhcmRpYW5fZW5yb2xsbWVudHMgY3JlYXRlOmd1YXJkaWFuX2Vucm9sbG1lbnRfdGlja2V0cyByZWFkOnVzZXJfaWRwX3Rva2VucyBjcmVhdGU6cGFzc3dvcmRzX2NoZWNraW5nX2pvYiBkZWxldGU6cGFzc3dvcmRzX2NoZWNraW5nX2pvYiByZWFkOmN1c3RvbV9kb21haW5zIGRlbGV0ZTpjdXN0b21fZG9tYWlucyBjcmVhdGU6Y3VzdG9tX2RvbWFpbnMgcmVhZDplbWFpbF90ZW1wbGF0ZXMgY3JlYXRlOmVtYWlsX3RlbXBsYXRlcyB1cGRhdGU6ZW1haWxfdGVtcGxhdGVzIHJlYWQ6bWZhX3BvbGljaWVzIHVwZGF0ZTptZmFfcG9saWNpZXMgcmVhZDpyb2xlcyBjcmVhdGU6cm9sZXMgZGVsZXRlOnJvbGVzIHVwZGF0ZTpyb2xlcyByZWFkOnByb21wdHMgdXBkYXRlOnByb21wdHMgcmVhZDpicmFuZGluZyB1cGRhdGU6YnJhbmRpbmciLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.HE1AJw69c4if0UbcZwrYiq6ttMPqBCa4BK0bNSW3SrQ4EWK-rcmWdYbWuz0uzDl6Lc9quvcMXAaDsALZws3o5XEBHdTwJsxJc_6hR3f9pjPlIEV1fELdXfJvkER6by6KPIsGMqWBixQdnWqy1no5Y7QhyqwzSJUOCcW7mN1JJpmA3l8U298_tsv5rrsXwNsk6Nkeco4TAScqKWfG7tpuW5L6klu7dZQwT9Tb8rOVcy_u5Ull29oAqVXBaEO6yosHu1SuLwCTGlX8TAYZbJYYH8g9MpW2jICqfa4sk4LAhj845PHV4IRe5yXLwU5Xdub2_sBp5_GeoTu8WDS8At4ikg'}
    // };
    
    // axios.get(options2.url, options2)
    // .then(function (response) {
    //   console.log((response.data));
    // })
    // request(options, function (error, response, body) {
    //   if (error) throw new Error(error);
    
    //   console.log(body,'useraaaaaaaaaa');
    // });

    var getUserOptions = {
      method: 'GET',
      url: 'http://localhost:3000/api/getUserRole/google-oauth2|100613204270669384478',
      qs: {q: 'email:"sarafiqu@uncg.edu"', search_engine: 'v3'},
      headers: {authorization: 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik9EQXpSVEV4TVRaQ1JqZ3lNVGc0TlRreE9VVTNOamREUlVFNE5UY3pSREUyTXprM05UUkJNZyJ9.eyJpc3MiOiJodHRwczovL2Rldi10ZXN0aW5nLWF1dGgwLmF1dGgwLmNvbS8iLCJzdWIiOiJWa2w4Q3g3WGdEM3pRWTB5dXNTcjVEYjJtZ2g1VVQ4dkBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9kZXYtdGVzdGluZy1hdXRoMC5hdXRoMC5jb20vYXBpL3YyLyIsImlhdCI6MTU3MDg0NzgyNywiZXhwIjoxNTcwOTM0MjI3LCJhenAiOiJWa2w4Q3g3WGdEM3pRWTB5dXNTcjVEYjJtZ2g1VVQ4diIsInNjb3BlIjoicmVhZDpjbGllbnRfZ3JhbnRzIGNyZWF0ZTpjbGllbnRfZ3JhbnRzIGRlbGV0ZTpjbGllbnRfZ3JhbnRzIHVwZGF0ZTpjbGllbnRfZ3JhbnRzIHJlYWQ6dXNlcnMgdXBkYXRlOnVzZXJzIGRlbGV0ZTp1c2VycyBjcmVhdGU6dXNlcnMgcmVhZDp1c2Vyc19hcHBfbWV0YWRhdGEgdXBkYXRlOnVzZXJzX2FwcF9tZXRhZGF0YSBkZWxldGU6dXNlcnNfYXBwX21ldGFkYXRhIGNyZWF0ZTp1c2Vyc19hcHBfbWV0YWRhdGEgY3JlYXRlOnVzZXJfdGlja2V0cyByZWFkOmNsaWVudHMgdXBkYXRlOmNsaWVudHMgZGVsZXRlOmNsaWVudHMgY3JlYXRlOmNsaWVudHMgcmVhZDpjbGllbnRfa2V5cyB1cGRhdGU6Y2xpZW50X2tleXMgZGVsZXRlOmNsaWVudF9rZXlzIGNyZWF0ZTpjbGllbnRfa2V5cyByZWFkOmNvbm5lY3Rpb25zIHVwZGF0ZTpjb25uZWN0aW9ucyBkZWxldGU6Y29ubmVjdGlvbnMgY3JlYXRlOmNvbm5lY3Rpb25zIHJlYWQ6cmVzb3VyY2Vfc2VydmVycyB1cGRhdGU6cmVzb3VyY2Vfc2VydmVycyBkZWxldGU6cmVzb3VyY2Vfc2VydmVycyBjcmVhdGU6cmVzb3VyY2Vfc2VydmVycyByZWFkOmRldmljZV9jcmVkZW50aWFscyB1cGRhdGU6ZGV2aWNlX2NyZWRlbnRpYWxzIGRlbGV0ZTpkZXZpY2VfY3JlZGVudGlhbHMgY3JlYXRlOmRldmljZV9jcmVkZW50aWFscyByZWFkOnJ1bGVzIHVwZGF0ZTpydWxlcyBkZWxldGU6cnVsZXMgY3JlYXRlOnJ1bGVzIHJlYWQ6cnVsZXNfY29uZmlncyB1cGRhdGU6cnVsZXNfY29uZmlncyBkZWxldGU6cnVsZXNfY29uZmlncyByZWFkOmVtYWlsX3Byb3ZpZGVyIHVwZGF0ZTplbWFpbF9wcm92aWRlciBkZWxldGU6ZW1haWxfcHJvdmlkZXIgY3JlYXRlOmVtYWlsX3Byb3ZpZGVyIGJsYWNrbGlzdDp0b2tlbnMgcmVhZDpzdGF0cyByZWFkOnRlbmFudF9zZXR0aW5ncyB1cGRhdGU6dGVuYW50X3NldHRpbmdzIHJlYWQ6bG9ncyByZWFkOnNoaWVsZHMgY3JlYXRlOnNoaWVsZHMgZGVsZXRlOnNoaWVsZHMgcmVhZDphbm9tYWx5X2Jsb2NrcyBkZWxldGU6YW5vbWFseV9ibG9ja3MgdXBkYXRlOnRyaWdnZXJzIHJlYWQ6dHJpZ2dlcnMgcmVhZDpncmFudHMgZGVsZXRlOmdyYW50cyByZWFkOmd1YXJkaWFuX2ZhY3RvcnMgdXBkYXRlOmd1YXJkaWFuX2ZhY3RvcnMgcmVhZDpndWFyZGlhbl9lbnJvbGxtZW50cyBkZWxldGU6Z3VhcmRpYW5fZW5yb2xsbWVudHMgY3JlYXRlOmd1YXJkaWFuX2Vucm9sbG1lbnRfdGlja2V0cyByZWFkOnVzZXJfaWRwX3Rva2VucyBjcmVhdGU6cGFzc3dvcmRzX2NoZWNraW5nX2pvYiBkZWxldGU6cGFzc3dvcmRzX2NoZWNraW5nX2pvYiByZWFkOmN1c3RvbV9kb21haW5zIGRlbGV0ZTpjdXN0b21fZG9tYWlucyBjcmVhdGU6Y3VzdG9tX2RvbWFpbnMgcmVhZDplbWFpbF90ZW1wbGF0ZXMgY3JlYXRlOmVtYWlsX3RlbXBsYXRlcyB1cGRhdGU6ZW1haWxfdGVtcGxhdGVzIHJlYWQ6bWZhX3BvbGljaWVzIHVwZGF0ZTptZmFfcG9saWNpZXMgcmVhZDpyb2xlcyBjcmVhdGU6cm9sZXMgZGVsZXRlOnJvbGVzIHVwZGF0ZTpyb2xlcyByZWFkOnByb21wdHMgdXBkYXRlOnByb21wdHMgcmVhZDpicmFuZGluZyB1cGRhdGU6YnJhbmRpbmciLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.HE1AJw69c4if0UbcZwrYiq6ttMPqBCa4BK0bNSW3SrQ4EWK-rcmWdYbWuz0uzDl6Lc9quvcMXAaDsALZws3o5XEBHdTwJsxJc_6hR3f9pjPlIEV1fELdXfJvkER6by6KPIsGMqWBixQdnWqy1no5Y7QhyqwzSJUOCcW7mN1JJpmA3l8U298_tsv5rrsXwNsk6Nkeco4TAScqKWfG7tpuW5L6klu7dZQwT9Tb8rOVcy_u5Ull29oAqVXBaEO6yosHu1SuLwCTGlX8TAYZbJYYH8g9MpW2jICqfa4sk4LAhj845PHV4IRe5yXLwU5Xdub2_sBp5_GeoTu8WDS8At4ikg'}
    };

    const userRole=await axios.get(getUserOptions.url, getUserOptions)
    .then(function (response) {
     return response.data
    })
    
  

    let pageProps = {};
    if (Component.getInitialProps) {
      pageProps = await Component.getInitialProps(ctx);
    }
    if (ctx.req && ctx.req.session.passport) {
      pageProps.user = ctx.req.session.passport.user;

      //This is so that it will only add the role if the user prop actualy exists
      if(pageProps.user) {
        pageProps.user.userRole=userRole
      }
      
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
   
    return (
      <React.Fragment>
        <Head>
          <title>{pageName}</title>
        </Head>
        <ThemeProvider theme={theme}>
          {/* CssBaseline kickstart an elegant, consistent, and simple baseline to build upon. */}
          <CssBaseline />
          <Layout user={this.state.user} pageName={pageName} >
          <Component user={this.state.user} {...pageProps} />
          </Layout>
          
        </ThemeProvider>
      </React.Fragment>
    );
  }
}
