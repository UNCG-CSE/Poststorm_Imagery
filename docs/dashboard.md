# Dashboard UI and Server 📊

**Document Updated:** {{ git_revision_date }}

A dashboard created so that researchers can apply tags to images so that we can
train a model to classify future images.

## Requirements 📝

The only requirement is **Node.js** which is a JavaScript runtime built on
Chrome's V8 JavaScript engine. Simply go to [here](https://nodejs.org/en/) and
download the latest version, *at this time **12.13.0 LTS***.

### Steps to set up enviroment

Now that you have Node installed you are going to need to install the packages.

1. Check that `node` and `npm` are installed with `node -v` and `npm -v`

2. Then go inside `Poststorm_Imagery\src\dashboard\v2` and using your
   favorite terminal run `npm install` to install all packages.

3. Now you need to determine if you want to run the Node servers with localhost
   or your machines IP address.

### Configure Auth0

the `v2` dashboard now has user authentication provived by Auth0. As such we have to add some configuration to get things working. At `Poststorm_Imagery\src\dashboard\v2` there will need to be a `.env` file that contains the following below.

```
PORT= Port to have the web server to be on

AUTH0_DOMAIN= The domain given by auth0
AUTH0_CLIENT_ID= Id so auth0 knows who this is
AUTH0_CLIENT_SECRET= secret key for authentication, DONT SHARE THIS EVER, LIKE EVER
AUTH0_CALLBACK_URL= call back route, for example http://localhost:3000/callback
BASE_URL= our sites base url, for example http://localhost:3000
```

Note, there is a file called `.env.template.txt` that contains this. The information for `AUTH0_DOMAIN`,`AUTH0_CLIENT_ID`,`AUTH0_CLIENT_SECRET` can all be obtained from the Auth0 website for the application.

### Running

After setting up the packages and setting up the `.env` file for Auth0 we can start up the webserver. Assuming your python paths for the `psic` modules are set you can simply run `npm run prod` to run the producton server. Then simply login in by creating your own account or using one of the Oauth methods provided. Currently the site is setup to run on `localhost` but changing the `.env` and `/src/server-config` files to use the machines IP will also work.

## Resources 💎

Post-Storm image tagging dashboard created using
[**Next.js**](https://nextjs.org/) for server side rendering of HTML pages,
[**React.js**](https://reactjs.org/) for UI development and
[**Node.js**](https://nodejs.org/) for the server side of things. Click the
names to follow to their websites.

## How It Works? 🤔

### Frontend

**Next.js** is a JavaScript framework that uses **React.js** to create the UI
and also renders the HTML server side before sending it to the client.

### Backend

The **Node.js** server is comprised of multiple parts. The main file, `server.js` mainly handles serving the **Next.js** pages. It also defines what pages, in our case folders, need the user to be logged in order to access. `auth-routes` is used to handle login/logut. The `/routes/api` page is used to handle all API calls such as getting image to tag or getting bearer token or posting the tag information for an image. Finally under `components/getBearerToken` we have the file that gets the bearer token for the application so that we can access certian information about users such as their roles.
