# Dashboard UI and Server 📊 <!-- omit in toc -->
A JavaScript developed and hosted dashboard to tag Post-Storm images.

## Table of Contents <!-- omit in toc -->

- [Requirements 📝](#requirements-)
- [Resources 💎](#resources-)
- [How it works 🤔](#how-it-works-)
	- [Frontend 📺](#frontend-)
	- [Backend 📡](#backend-)

## Requirements 📝

The only requirement is **Node.js** which is JavaScript ran by Chrome's V8 JavaScript engine to basicly allow JavaScript to be ran server side. Simply go to [here](https://nodejs.org/en/) and download the latest version, *at this time **10.16.3 LTS***.

Now that you have **Node.js** installed you will see 2 folders, `node_server` and `web_server`. To install packages run `npm install` while inside the folder which will install all packages needed. For **Node.js** `package.json` is basicly like `pipfile` and manages all your dependicies and additional utiliy scripts and project meta data.

Starting with `node_server`, after installing packages run `node server.js` which will run `server.js` and start the server at `YOUR_IP:4000`.

Now for `web_server` run `npm run dev` which basicly runs a script called `dev` in the `package.json` which runs **Next.js** and starts rendering and sending the HTML page to the user. This will run the webserver on `YOUR_IP:3000`. **NOTE** this currently does not work due to the web server needing to connect to a specific IP for the node server, so for now I have to have a Google VM running to act as the server.



## Resources 💎
Post-Storm image tagging dashboard created using **Next.js** for server side rendering of HTML pages, **React.js** for UI development and **Node.js** for the server side of things.

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
<a href="https://nodejs.org/">
	<kbd>
		<img src="https://nodejs.org/static/images/logos/nodejs-new-pantone-black.png" width="64">
	</kbd>
</a>


</p>


<p align="center">
  
</p>

## How it works 🤔

### Frontend 📺
**Next.js** is a JavaScript framework that uses **React.js** to create the UI and also enable it to be rendered on the server side.

### Backend 📡
**Node.js** has two tasks. The first task is for **Node.js** to generate a unique route for compressed and uncompressed image and store this list and interact with a database. The second task is for **Node.js** to run **Next.js** whenever a user connects to the site. Once a user requests a image **Node.js** will leverage the information from the first task and randomly select an availible image and attach that link to the server side rendered HTML and then send it to the user.

Since **Node.js** is a  single-threaded, non-blocking, asynchronously program, the first and second tasks are broken up into 2 **Node.js** servers to improve performance,but is still on the same machine.
