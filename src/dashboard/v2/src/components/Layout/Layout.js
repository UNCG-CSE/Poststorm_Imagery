import React,{forwardRef} from 'react';
import PropTypes from 'prop-types';

import CssBaseline from '@material-ui/core/CssBaseline';
import Drawer from '@material-ui/core/Drawer';
import Hidden from '@material-ui/core/Hidden';
import Typography from '@material-ui/core/Typography';
import { makeStyles, useTheme } from '@material-ui/core/styles';

import MyTheme from '../theme';
import SideDrawer from './SideDrawer'
import AppBar from './MyAppBar'

import Link from "next/link";

import Styles from '../Styles'

const useStyles = makeStyles(theme => ({
  root: {
    display: 'flex',
    
  },
  drawer: {
    [theme.breakpoints.up('sm')]: {
      width: Styles.drawerWidth,
      flexShrink: 0,
    },
    
  },
  toolbar: theme.mixins.toolbar,
  drawerPaper: {
    width: Styles.drawerWidth,
    
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing(3),
    
  },
}));

function ResponsiveDrawer(props) {

  const { container } = props;
  const classes = useStyles();
  const theme = useTheme();
  const [mobileOpen, setMobileOpen] = React.useState(false);
  const hasUser=props.user !==undefined

  // console.log((props.user))

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const show_drawer = () => {
    return (
      <>
        <SideDrawer user={props.user}/>
      </>
    )
  }
  // function show_drawer() {
  //   return ()
  // }

  return (
    <div className={classes.root}>
      <CssBaseline />
      <AppBar handleToggle={handleDrawerToggle} pageName={props.pageName}/>
      <nav className={classes.drawer} aria-label="mailbox folders">      
        {/* The implementation can be swapped with js to avoid SEO duplication of links. */}
        <Hidden smUp implementation="css">
          <Drawer
            container={container}
            variant="temporary"
            anchor={theme.direction === 'rtl' ? 'right' : 'left'}
            open={mobileOpen}
            onClose={handleDrawerToggle}
            classes={{
              paper: classes.drawerPaper,
            }}
            ModalProps={{
              keepMounted: true, // Better open performance on mobile.
            }}
          >
            {show_drawer()}
          </Drawer>
        </Hidden>
        <Hidden xsDown implementation="css">
          <Drawer
            classes={{
              paper: classes.drawerPaper,
            }}
            variant="permanent"
            open
          >
            {show_drawer()}
          </Drawer>
        </Hidden>
      </nav>
      <main className={classes.content}>
        <div className={classes.toolbar} />
        <div>
          {props.children}
          
        </div>
        {/* <Typography paragraph>
          {JSON.stringify(props.user)}
          {'Is logged in?: '+hasUser}
        </Typography> */}
      
      </main>
    </div>
  );
}

ResponsiveDrawer.propTypes = {
  /**
   * Injected by the documentation to work in an iframe.
   * You won't need it on your project.
   */
  container: PropTypes.instanceOf(typeof Element === 'undefined' ? Object : Element),
};

export default ResponsiveDrawer;