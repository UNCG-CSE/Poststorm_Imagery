import React from 'react';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import Divider from '@material-ui/core/Divider';
import TreeView from '@material-ui/lab/TreeView';
import StyledTreeItem from './../TreeItem'
import Link from "next/link";
import MyTheme from '../../theme';
//icons
import ArrowDropDownIcon from '@material-ui/icons/ArrowDropDown';
import ArrowRightIcon from '@material-ui/icons/ArrowRight';
//signin icon
import ExitToAppIcon from '@material-ui/icons/ExitToApp';
import LockIcon from '@material-ui/icons/Lock';
import ImageIcon from '@material-ui/icons/Image';

import Styles from '../../Styles'
import Tab from '@material-ui/core/Tab';


const useStyles = makeStyles(theme => ({
  rootTree: {
    height: 264,
    flexGrow: 1,
   
    maxWidth: 400,
  },
  toolbar: theme.mixins.toolbar,
  drawerPaper: {
    width: Styles.drawerWidth,
    
  },
}));

export default function notLoggedIn(props) {
  const classes = useStyles();
  const hasUser=props.user !==undefined;

  return (
    <div>
        <Link href="/login">
          <StyledTreeItem 
            nodeId="1" labelText="Signin" labelIcon={LockIcon} 
            // myClickedBackgroundColor={MyTheme.palette.grey100.color} 
            // //myHoverBackgroundColor={MyTheme.palette.red500.color} 
            // myTextColor={MyTheme.palette.primary.main} 
            // myHoverTextColor={MyTheme.palette.grey100.color} 
            // myClickedTextColor={MyTheme.palette.primary.main} 
          />
        </Link>
    </div>
  );
}
