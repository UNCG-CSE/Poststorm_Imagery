# Dashboard UI and Server 📊 <!-- omit in toc -->

A JavaScript developed and hosted dashboard to tag Post-Storm images.

## Table of Contents <!-- omit in toc -->

- [Requirements 📝](#requirements-)
	- [Steps to Reproduce 🔎](#steps-to-reproduce-)
- [Resources 💎](#resources-)
- [How It Works 🤔](#how-it-works-)
	- [Frontend 📺](#frontend-)
	- [Backend 📡](#backend-)
	- [Database 🗄️](#database-️)

## Requirements 📝

The first requirement is **Node.js** which is JavaScript ran by Chrome's V8 JavaScript engine to basicly allow JavaScript to be ran server side. Simply go to [here](https://nodejs.org/en/) and download the latest version, *at this time **10.16.3 LTS***.

~~The second requirment is to have `npm-run-all` package installed globally. Run this command anywhere `npm install -g npm-run-all`~~

### Steps to Reproduce 🔎

1. Check that `node` and `npm` are installed with `node -v` and `npm -v`

2. Move to `web_server` folder and using your favorite terminal run `npm install` or `npm i` to install all packages.

From here you have two choices, only run one at a time.

1. To run off **localhost** run `npm run localhost` which will start both the web and node server on their respective ports on localhost.

2. To run of the **machines IP**, run `npm run useIP` which will run the node and web server off your machines IP.

## Resources 💎

- **Next.js** is a framework for **React.js** that has the ability to render the HTML pages server side.
  
- **React.js** is a JavaScript library for building UI components.

- **Matieral-UI** is a set of React components that impliment Googles Matieral Design specifications from [here](https://material.io/design/introduction/)

- **Node.js** is a JavaScript run time enviroment that runs JavaScript outside a browser and basicly allows for JavaScript to be ran as a server.

Links to the resources can be found here.

<p >

<a href="https://nextjs.org/">
	<kbd>
		<img src="https://seeklogo.com/images/N/next-js-logo-7929BCD36F-seeklogo.com.png" width="64">
	</kbd>
</a>
<a href="https://reactjs.org/">
	<kbd>
		<img src="https://cdn4.iconfinder.com/data/icons/logos-3/600/React.js_logo-512.png" width="48">
	</kbd>
</a>
<a href="https://material-ui.com/">
	<kbd>
		<img src="https://material-ui.com/static/images/material-ui-logo.svg" width="48">
	</kbd>
</a>

<a href="https://nodejs.org/">
	<kbd>
		<img src="https://nodejs.org/static/images/logos/nodejs-new-pantone-black.png" width="64">
	</kbd>
</a>


</p>


<p align="center">
  
</p>

## How It Works 🤔

There are technically two servers, one I will refer to as the **web server** since it deals with sending the HTML pages to the client and the other as **node server** as it deals with creating and handling all the API calls,interaction with the database and handling responces from the client. The servers are broken up like to seperate concerns and allow the **web server** and **node server** to be on seperate machines.

### Frontend 📺

**Next.js** is a JavaScript framework that uses **React.js** to create the UI and also enable it to be rendered on the server side. Since **Next.js** allows for server side rendering, before being sent to the client, **Next.js** will communicate with the node server to gather initial values and then send that end result to the client. **Material-UI** helps make the dashboard look nice.

### Backend 📡

TBD reworked

~~**Node.js** has two tasks. The first task is for **Node.js** to generate a unique route for compressed and uncompressed image and store this list and interact with a database. The second task is for **Node.js** to run **Next.js** whenever a user connects to the site. Once a user requests a image **Node.js** will leverage the information from the first task and randomly select an availible image and attach that link to the server side rendered HTML and then send it to the user.~~

~~Since **Node.js** is a  single-threaded, non-blocking, asynchronously program, the first and second tasks are broken up into 2 **Node.js** servers to improve performance since they will run on 2 threads,but is still on the same machine.~~

### Database 🗄️

TBD 😢
