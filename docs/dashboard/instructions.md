# Dashboard UI and Server 📊

**Document Updated:** {{ git_revision_date }}

A dashboard created so that researchers can apply tags to images so that we can
train a model to classify future images.

## Requirements 📝

The only requirement is **Node.js** which is a JavaScript runtime built on
Chrome's V8 JavaScript engine. Simply go to [here](https://nodejs.org/en/) and
download the latest version, *at this time **12.13.0 LTS***.

## Setting Up The Environment

Now that you have Node installed you are going to need to install the packages.

1. Check that `node` and `npm` are installed with `node -v` and `npm -v`

2. Then go inside `src/dashboard/v2` and using your
   favorite terminal run `npm install` to install all packages.

3. Now you need to determine if you want to run the Node servers with localhost
   or your machines IP address.

## Configure Auth0

the `v2` dashboard now has user authentication provided by Auth0. As such we have to add some configuration to get
things working. At `src/dashboard/v2` a file called `.env` should exist that contains the following contents:

```dotenv
PORT=3000  # The port of the server to run on

AUTH0_DOMAIN=  # The domain of the authenticator
AUTH0_CLIENT_ID=  # The admin's ID
AUTH0_CLIENT_SECRET=  # The admin's secret

BASE_IP=localhost  # The IP to run the server on
BASE_URL=http://localhost:3000  # The URL of the server (include http/https and port)
AUTH0_CALLBACK_URL=http://localhost:3000/callback  # The callback URL for logout (same as BASE_URL, but with /callback)

ASSIGNER_SCRIPT=assign_batch.py
ASSIGNER_SOURCE=../../python/psic/assigner/
IMAGE_SOURCE=/home/matmorcat/P-Sick/

FULL_SIZE_IMAGE_PATH=/home/matmorcat/P-Sick/data/Florence  # The scope path to where the catalog.csv should exist
SMALL_SIZE_IMAGE_PATH=/home/matmorcat/P-Sick/small/Florence  # The scope path to the small version of the above

# The IP in src/dashboard/v2/src/server-config.js must also be changed to the same value used here!
```

!!! Note
    There is a file called `.env.template.txt` that contains the above information. The values for
    `AUTH0_DOMAIN`,`AUTH0_CLIENT_ID`,`AUTH0_CLIENT_SECRET` can all be obtained from the Auth0 website for the
    application. You may copy this file and rename it to `.env` then modify the values as needed.

## Configuring Python Path

Follow the steps at [**Configuring Module**](../configure_python_path.md)

## Running

After setting up the packages and setting up the `.env` file for Auth0 we can start up the host server.
Assuming your python paths for the `psic` modules are set you can simply run `npm run prod` to run the production
server. Then simply login in by creating your own account or using one of the Oauth methods provided. Currently the site is setup to run on `localhost` but changing the `.env` and `/src/server-config` files to use the machines IP will also work.

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
