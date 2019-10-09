import React from 'react';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';

import MyTheme from './theme';

import Styles from './Styles'

// const useStyles = Styles.useStyles;
const drawerWidth = 240;

const useStyles = makeStyles(theme => ({
    appBar: {
      marginLeft: drawerWidth,
      [theme.breakpoints.up('sm')]: {
        width: `calc(100% - ${drawerWidth}px)`,
      },
      backgroundColor:MyTheme.palette.pukeGreenBG.backgroundColor
    },
    ...Styles.useStyles,
    menuButton: {
      marginRight: theme.spacing(2),
      [theme.breakpoints.up('sm')]: {
        display: 'none',
      },
    },
    toolbar: theme.mixins.toolbar,
}));
  

export default function MyAppBar(props) {
  const classes = useStyles(); 
    return (
        <AppBar position="fixed" className={classes.appBar}>
            <Toolbar>
            <IconButton
                color="inherit"
                aria-label="open drawer"
                edge="start"
                onClick={props.handleToggle}
                className={classes.menuButton}
            >
                <MenuIcon />
            </IconButton>
            <Typography variant="h6" noWrap>
                { props.pageName ||'Post Storm Image Classification Dashboard'}
            </Typography>
            </Toolbar>
        </AppBar>
    );
  }
