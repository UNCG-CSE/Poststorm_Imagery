
require("dotenv").config();
const express = require("express");//package for networking
const http = require("http");
const next = require("next");//The react framework for server side rendering
const session = require("express-session");
const bodyParser = require('body-parser');

const serverConfig =require('./server-config')
// 1 - importing dependencies
const passport = require("passport");
const Auth0Strategy = require("passport-auth0");
const uid = require('uid-safe');
const authRoutes = require("./auth-routes");

//routing modules
const apiRoutes = require("./routes/api");

//For Nextjs
const dev = process.env.NODE_ENV !== "production";
console.log(`Is in dev mode? ${dev}`)

//This is used to change where src is, since in production the .next folder will be one level above
// the ./src folder.
const get_dir = dev => dev ? './src':'./'

const app = next({
  dev,
  dir: get_dir(dev)
});
const handle = app.getRequestHandler();

app.prepare().then(async () => {
  const server = express();
  const IP= await serverConfig.getIp()

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
    next();
  };

  server.use(function(req, res, next) {
      res.header("Access-Control-Allow-Origin", "*");
      res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
      next();
  });

  server.use(bodyParser.urlencoded({ extended: false }));
  server.use(express.json());
  
  // For these routes,restrict access :)
  server.use("/auth", restrictAccess);

  server.use("/api", apiRoutes);
  
  // handling everything else with Next.js
  server.get("*", handle);

  //Say when and where server is up
  http.createServer(server).listen(process.env.PORT,'0.0.0.0', () => {
    console.log(`>>> Site up on http://${IP}:${process.env.PORT}`);
  });
});
