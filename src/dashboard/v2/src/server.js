
require("dotenv").config();
const express = require("express");
const http = require("http");
const next = require("next");
const session = require("express-session");
// 1 - importing dependencies
const passport = require("passport");
const Auth0Strategy = require("passport-auth0");
const uid = require('uid-safe');
const authRoutes = require("./auth-routes");

//routing modules
const apiRoutes = require("./routes/api");

//For Nextjs
const dev = process.env.NODE_ENV !== "production";
const app = next({
  dev,
  dir: "./src"
});
const handle = app.getRequestHandler();

// var request = require("request");



app.prepare().then(() => {
  const server = express();

  // 2 - add session management to Express
  const sessionConfig = {
    secret: uid.sync(18),
    cookie: {
      maxAge: 86400 * 1000 // 24 hours in milliseconds
    },
    resave: false,
    saveUninitialized: true
  };
  server.use(session(sessionConfig));

  // 3 - configuring Auth0Strategy
  const auth0Strategy = new Auth0Strategy(
    {
      domain: process.env.AUTH0_DOMAIN,
      clientID: process.env.AUTH0_CLIENT_ID,
      clientSecret: process.env.AUTH0_CLIENT_SECRET,
      callbackURL: process.env.AUTH0_CALLBACK_URL
    },
    function(accessToken, refreshToken, extraParams, profile, done) {
      return done(null, profile);
    }
  );

  // 4 - configuring Passport
  passport.use(auth0Strategy);
  passport.serializeUser((user, done) => done(null, user));
  passport.deserializeUser((user, done) => done(null, user));

  // 5 - adding Passport and authentication routes
  server.use(passport.initialize());
  server.use(passport.session());
  server.use(authRoutes);

  // 6 - you are restricting access to some routes
  const restrictAccess = (req, res, next) => {
    
    if (!req.isAuthenticated()){
      return res.redirect("/login");
    } 

    //https://auth0.com/docs/users/search/v3/get-users-endpoint
    // var options = {
    //   method: 'GET',
    //   url: 'https://dev-testing-auth0.auth0.com/api/v2/users',
    //   qs: {q: 'email:"jane@exampleco.com"', search_engine: 'v3'},
    //   headers: {authorization: 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik9EQXpSVEV4TVRaQ1JqZ3lNVGc0TlRreE9VVTNOamREUlVFNE5UY3pSREUyTXprM05UUkJNZyJ9.eyJpc3MiOiJodHRwczovL2Rldi10ZXN0aW5nLWF1dGgwLmF1dGgwLmNvbS8iLCJzdWIiOiJWa2w4Q3g3WGdEM3pRWTB5dXNTcjVEYjJtZ2g1VVQ4dkBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9kZXYtdGVzdGluZy1hdXRoMC5hdXRoMC5jb20vYXBpL3YyLyIsImlhdCI6MTU3MDg0NzgyNywiZXhwIjoxNTcwOTM0MjI3LCJhenAiOiJWa2w4Q3g3WGdEM3pRWTB5dXNTcjVEYjJtZ2g1VVQ4diIsInNjb3BlIjoicmVhZDpjbGllbnRfZ3JhbnRzIGNyZWF0ZTpjbGllbnRfZ3JhbnRzIGRlbGV0ZTpjbGllbnRfZ3JhbnRzIHVwZGF0ZTpjbGllbnRfZ3JhbnRzIHJlYWQ6dXNlcnMgdXBkYXRlOnVzZXJzIGRlbGV0ZTp1c2VycyBjcmVhdGU6dXNlcnMgcmVhZDp1c2Vyc19hcHBfbWV0YWRhdGEgdXBkYXRlOnVzZXJzX2FwcF9tZXRhZGF0YSBkZWxldGU6dXNlcnNfYXBwX21ldGFkYXRhIGNyZWF0ZTp1c2Vyc19hcHBfbWV0YWRhdGEgY3JlYXRlOnVzZXJfdGlja2V0cyByZWFkOmNsaWVudHMgdXBkYXRlOmNsaWVudHMgZGVsZXRlOmNsaWVudHMgY3JlYXRlOmNsaWVudHMgcmVhZDpjbGllbnRfa2V5cyB1cGRhdGU6Y2xpZW50X2tleXMgZGVsZXRlOmNsaWVudF9rZXlzIGNyZWF0ZTpjbGllbnRfa2V5cyByZWFkOmNvbm5lY3Rpb25zIHVwZGF0ZTpjb25uZWN0aW9ucyBkZWxldGU6Y29ubmVjdGlvbnMgY3JlYXRlOmNvbm5lY3Rpb25zIHJlYWQ6cmVzb3VyY2Vfc2VydmVycyB1cGRhdGU6cmVzb3VyY2Vfc2VydmVycyBkZWxldGU6cmVzb3VyY2Vfc2VydmVycyBjcmVhdGU6cmVzb3VyY2Vfc2VydmVycyByZWFkOmRldmljZV9jcmVkZW50aWFscyB1cGRhdGU6ZGV2aWNlX2NyZWRlbnRpYWxzIGRlbGV0ZTpkZXZpY2VfY3JlZGVudGlhbHMgY3JlYXRlOmRldmljZV9jcmVkZW50aWFscyByZWFkOnJ1bGVzIHVwZGF0ZTpydWxlcyBkZWxldGU6cnVsZXMgY3JlYXRlOnJ1bGVzIHJlYWQ6cnVsZXNfY29uZmlncyB1cGRhdGU6cnVsZXNfY29uZmlncyBkZWxldGU6cnVsZXNfY29uZmlncyByZWFkOmVtYWlsX3Byb3ZpZGVyIHVwZGF0ZTplbWFpbF9wcm92aWRlciBkZWxldGU6ZW1haWxfcHJvdmlkZXIgY3JlYXRlOmVtYWlsX3Byb3ZpZGVyIGJsYWNrbGlzdDp0b2tlbnMgcmVhZDpzdGF0cyByZWFkOnRlbmFudF9zZXR0aW5ncyB1cGRhdGU6dGVuYW50X3NldHRpbmdzIHJlYWQ6bG9ncyByZWFkOnNoaWVsZHMgY3JlYXRlOnNoaWVsZHMgZGVsZXRlOnNoaWVsZHMgcmVhZDphbm9tYWx5X2Jsb2NrcyBkZWxldGU6YW5vbWFseV9ibG9ja3MgdXBkYXRlOnRyaWdnZXJzIHJlYWQ6dHJpZ2dlcnMgcmVhZDpncmFudHMgZGVsZXRlOmdyYW50cyByZWFkOmd1YXJkaWFuX2ZhY3RvcnMgdXBkYXRlOmd1YXJkaWFuX2ZhY3RvcnMgcmVhZDpndWFyZGlhbl9lbnJvbGxtZW50cyBkZWxldGU6Z3VhcmRpYW5fZW5yb2xsbWVudHMgY3JlYXRlOmd1YXJkaWFuX2Vucm9sbG1lbnRfdGlja2V0cyByZWFkOnVzZXJfaWRwX3Rva2VucyBjcmVhdGU6cGFzc3dvcmRzX2NoZWNraW5nX2pvYiBkZWxldGU6cGFzc3dvcmRzX2NoZWNraW5nX2pvYiByZWFkOmN1c3RvbV9kb21haW5zIGRlbGV0ZTpjdXN0b21fZG9tYWlucyBjcmVhdGU6Y3VzdG9tX2RvbWFpbnMgcmVhZDplbWFpbF90ZW1wbGF0ZXMgY3JlYXRlOmVtYWlsX3RlbXBsYXRlcyB1cGRhdGU6ZW1haWxfdGVtcGxhdGVzIHJlYWQ6bWZhX3BvbGljaWVzIHVwZGF0ZTptZmFfcG9saWNpZXMgcmVhZDpyb2xlcyBjcmVhdGU6cm9sZXMgZGVsZXRlOnJvbGVzIHVwZGF0ZTpyb2xlcyByZWFkOnByb21wdHMgdXBkYXRlOnByb21wdHMgcmVhZDpicmFuZGluZyB1cGRhdGU6YnJhbmRpbmciLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.HE1AJw69c4if0UbcZwrYiq6ttMPqBCa4BK0bNSW3SrQ4EWK-rcmWdYbWuz0uzDl6Lc9quvcMXAaDsALZws3o5XEBHdTwJsxJc_6hR3f9pjPlIEV1fELdXfJvkER6by6KPIsGMqWBixQdnWqy1no5Y7QhyqwzSJUOCcW7mN1JJpmA3l8U298_tsv5rrsXwNsk6Nkeco4TAScqKWfG7tpuW5L6klu7dZQwT9Tb8rOVcy_u5Ull29oAqVXBaEO6yosHu1SuLwCTGlX8TAYZbJYYH8g9MpW2jICqfa4sk4LAhj845PHV4IRe5yXLwU5Xdub2_sBp5_GeoTu8WDS8At4ikg'}
    // };
    
    // request(options, function (error, response, body) {
    //   if (error) throw new Error(error);
    
    //   console.log(body,'user');
    // });
  
    //
    //console.log(req.user)
    next();
  };

  // For these routes,restrict access :)
  server.use("/protected", restrictAccess);
  server.use("/tagImage", restrictAccess);

  server.use("/api", apiRoutes);
  

  // handling everything else with Next.js
  server.get("*", handle);

  http.createServer(server).listen(process.env.PORT, () => {
    console.log(`listening on port ${process.env.PORT}`);
  });
});
