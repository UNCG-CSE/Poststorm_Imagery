# Source Files Structure

The first thing I will go over is the folder structure and what each important file does.

## Folder  Structure

```
v2/
│   .babelrc
│   .env
│   .env.template.txt
│   .eslintignore
│   .eslintrc.json
│   .gitignore
│   next.config.js
│   package-lock.json
│   package.json
│   readme.md
│
└───src/
    │   auth-routes.js
    │   server-config.js
    │   server.js
    │
    ├───.next
    │
    ├───components/
    │   │   CenterGrid.js
    │   │   getBearerToken.js
    │   │   Link.js
    │   │   routeToPageName.js
    │   │   Styles.js
    │   │   theme.js
    │   │
    │   ├───image_tagging/
    │   │       displayImage.js
    │   │
    │   └───Layout/
    │       │   Layout.js
    │       │   MyAppBar.js
    │       │   SideDrawer.js
    │       │   TreeItem.js
    │       │
    │       └───sideDrawerGroups/
    │               loggedIn.js
    │               notLoggedIn.js
    │
    ├───pages/
    │   │   index.js
    │   │   _app.js
    │   │   _document.js
    │   │
    │   └───auth/
    │           tagImage.js
    │
    └───routes/
            api.js
            test.js
```

## Root (`v2`)

Starting with the `.env` file, ***IT IS VERY IMPORTANT THAT THIS FILE IS NEVER SHARED***. This file contains the
application secret ID that the authentication service uses so that the authentication services knows that this server
is legitimate app. It has things such that client secret defined, what port to use, IP, callback address for when users
logout, and the base URL. To see the format for the `.env` file take a look at `.env.template.txt`

`next.config.js` file is used by *Next.js* and its main function is to help parse the `.env` file mentioned above.

`package.json` keeps track of all packages and versions for a *Node.js* project. It also has information such dev
dependencies, project information like github repo, project name, project version, and scripts such as `npm run dev`
which runs the development version of the Node server. If you ran `npm install`, the command will look for a
`package.json` to find what packages to install and if it didn't find a `package.json` it would create a bare bones
file with project details.

`package-lock.json` is used to lock those dependencies to a specific version.

### Source Code (`src`)

This is where the real content of the Dashboard is.
