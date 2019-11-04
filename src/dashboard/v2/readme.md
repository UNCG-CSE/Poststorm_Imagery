# Source documentation for Dashboard

The first thing I will go over is the file structure and what each important file does.

## File Structure

Dont worry about any files that are crossed out, that just means they are not too critical to learn about but still exist.
```
v2  
│   ~.babelrc~  
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
└───src  
    │   auth-routes.js  
    │   server-config.js  
    │   server.js  
    │  
    ├───.next  
    │  
    ├───components  
    │   │   CenterGrid.js  
    │   │   getBearerToken.js  
    │   │   Link.js  
    │   │   routeToPageName.js  
    │   │   Styles.js  
    │   │   theme.js  
    │   │  
    │   ├───image_tagging  
    │   │       displayImage.js  
    │   │  
    │   └───Layout
    │       │   Layout.js  
    │       │   MyAppBar.js  
    │       │   SideDrawer.js  
    │       │   TreeItem.js  
    │       │  
    │       └───sideDrawerGroups  
    │               loggedIn.js  
    │               notLoggedIn.js  
    │     
    ├───pages  
    │   │   index.js  
    │   │   _app.js  
    │   │   _document.js  
    │   │  
    │   └───auth  
    │           tagImage.js  
    │  
    └───routes  
            api.js  
            test.js  
```