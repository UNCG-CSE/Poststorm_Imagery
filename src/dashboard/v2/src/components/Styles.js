import { makeStyles, useTheme } from '@material-ui/core/styles';
import MyTheme from './theme';

module.exports = (function() {
    const drawerWidth = 240;
    const useStyles = makeStyles(theme => ({
        rootTree: {
          height: 264,
          flexGrow: 1,
         
          maxWidth: 400,
        },
        root: {
          display: 'flex',
          
        },
        drawer: {
          [theme.breakpoints.up('sm')]: {
            width: drawerWidth,
            flexShrink: 0,
          },
          
        },
        // appBar: {
        //   marginLeft: drawerWidth,
        //   [theme.breakpoints.up('sm')]: {
        //     width: `calc(100% - ${drawerWidth}px)`,
        //   },
        //   backgroundColor:MyTheme.palette.pukeGreenBG.backgroundColor
        // },
        menuButton: {
          marginRight: theme.spacing(2),
          [theme.breakpoints.up('sm')]: {
            display: 'none',
          },
          
        },
        toolbar: theme.mixins.toolbar,
        drawerPaper: {
          width: drawerWidth,
          
        },
        content: {
          flexGrow: 1,
          padding: theme.spacing(3),
          
        },
        buttonTree: {
          margin: theme.spacing(1,0,0,-1),
          
        },
        logoutButton:{
          margin: theme.spacing(1,0,1,0),
          backgroundColor:MyTheme.palette.error.main
        }
      }));
    return { 
        drawerWidth,
        useStyles:useStyles
    };

})();
