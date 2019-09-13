# Dashboard UI and Server 📊 <!-- omit in toc -->
A JavaScript developed and hosted dashboard to tag Post-Storm images.

## Table of Contents <!-- omit in toc -->

- [Requirements 📝](#requirements-)
	- [Steps to Reproduce 🔎](#steps-to-reproduce-)
- [Resources 💎](#resources-)
- [How It Works 🤔](#how-it-works-)
	- [Frontend 📺](#frontend-)
	- [Backend 📡](#backend-)

## Requirements 📝

The only requirement is **Node.js** which is JavaScript ran by Chrome's V8 JavaScript engine to basicly allow JavaScript to be ran server side. Simply go to [here](https://nodejs.org/en/) and download the latest version, *at this time **10.16.3 LTS***.

### Steps to Reproduce 🔎

1. Check that `node` and `npm` are installed with `node -v` and `npm -v`

2. Move to `web_server` folder and using your favorite terminal run `npm install` to install all packages. 

3. Determine if you want to run both node servers off localhost or your machines IP.

From here you have two choices 

1. To run off **localhost** run `npm run web` to run the web server and `npm run node` to run the image server. Then connect to `http://localhost:3000/` for the website or `http://localhost:4000/` to see the image server working

2. To run of the **machines IP**, run `npm run web-host` and `npm run node-host`. Then connect to `http://<YOUR IP>:3000/` for website or `http://<YOUR IP>:4000/` for image server.

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

## How It Works 🤔

### Frontend 📺
**Next.js** is a JavaScript framework that uses **React.js** to create the UI and also enable it to be rendered on the server side.

### Backend 📡
**Node.js** has two tasks. The first task is for **Node.js** to generate a unique route for compressed and uncompressed image and store this list and interact with a database. The second task is for **Node.js** to run **Next.js** whenever a user connects to the site. Once a user requests a image **Node.js** will leverage the information from the first task and randomly select an availible image and attach that link to the server side rendered HTML and then send it to the user.

Since **Node.js** is a  single-threaded, non-blocking, asynchronously program, the first and second tasks are broken up into 2 **Node.js** servers to improve performance since they will run on 2 threads,but is still on the same machine.
