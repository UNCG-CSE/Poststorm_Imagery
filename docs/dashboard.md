# Dashboard UI and Server 📊

A dashboard created so that researchers can apply tags to images so that we can
train a model to classify future images.

## Requirements 📝

The only requirement is **Node.js** which is a JavaScript runtime built on
Chrome's V8 JavaScript engine. Simply go to [here](https://nodejs.org/en/) and
download the latest version, *at this time **10.16.3 LTS***.

### Steps to Reproduce

Now that you have Node installed you are going to need to install the packages.

1. Check that `node` and `npm` are installed with `node -v` and `npm -v`

2. Then go inside `Poststorm_Imagery\src\dashboard\web_server` and using your
   favorite terminal run `npm install` to install all packages.

3. Now you need to determine if you want to run the Node servers with localhost
   or your machines IP address.

#### Localhost

To run off **localhost** execute the command `npm run localhost`. Then connect
to `http://localhost:3000/` for the website or `http://localhost:4000/` to see
the node-image server. In the event that port 3000 and 4000 are not used, the
terminal will always display the correct URL to follow.

#### IP address

To run off **IP address** execute the command `npm run useIP`. . Then connect to
`http://<YOUR IP>:3000/` for website or `http://<YOUR IP>:4000/` for node-image
server. In the event that port 3000 and 4000 are not used, the terminal will
always display the correct URL to follow.

## Resources 💎

Post-Storm image tagging dashboard created using
[**Next.js**](https://nextjs.org/) for server side rendering of HTML pages,
[**React.js**](https://reactjs.org/) for UI development and
[**Node.js**](https://nodejs.org/) for the server side of things. Click the
names to follow to their websites.

## How It Works? 🤔

### Frontend 📺

**Next.js** is a JavaScript framework that uses **React.js** to create the UI
and also renders the HTML server side before sending it to the client.

### Backend 📡

There are two **Node.js** servers. The first one is tasked with rendering the
HTML page and sending it down to the client. The second is responsible for
interacting with the database and handling submitions from the client. They are
seperated out to run on differnt threads and seperate code out.
