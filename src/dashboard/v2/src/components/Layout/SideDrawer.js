import React from 'react';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import Divider from '@material-ui/core/Divider';
import TreeView from '@material-ui/lab/TreeView';
import StyledTreeItem from './TreeItem'
import Link from "next/link";
import MyTheme from '../theme';
//icons
import ArrowDropDownIcon from '@material-ui/icons/ArrowDropDown';
import ArrowRightIcon from '@material-ui/icons/ArrowRight';
//signin icon
import ExitToAppIcon from '@material-ui/icons/ExitToApp';
import LockIcon from '@material-ui/icons/Lock';
import ImageIcon from '@material-ui/icons/Image';

import Styles from '../Styles'
import Tab from '@material-ui/core/Tab';


import NotLoggedIn from './sideDrawerGroups/notLoggedIn'
import LoggedIn from './sideDrawerGroups/loggedIn'
import { func } from 'prop-types';

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



export default function SideDrawer(props) {
  const classes = useStyles();
  const hasUser=props.user !==undefined;

  function handleLoggedIn() {
    if(hasUser) {
      return <LoggedIn/>
    }
    return <NotLoggedIn/>
  }

  let userRole='N/A'

  //Incase something goes big sad :(
  try {
    userRole=props.user.userRole.data[0].name

  }
  catch(err) {
   
    //console.log(err.message)
  }
  
  function generateUserRoleName() {
    if(props.user) {
      if(props.user.nickname) {
        return `, ${userRole}: ${props.user.nickname}`
      }
    }
    return '' 
  }
 

  const username= hasUser ? ','+props.user.nickname: '' 
  const role= hasUser ? ',': '' //props.user.userRole.data[0].name


  return (
    <div>
      <div className={classes.toolbar} />
      <Divider />
      <Tab label={"Welcome"+generateUserRoleName()} disableRipple/>
      <Divider />
      <TreeView
        className={classes.rootTree}
        defaultExpanded={['3']}
        defaultCollapseIcon={<ArrowDropDownIcon />}
        defaultExpandIcon={<ArrowRightIcon />}
        defaultEndIcon={<div style={{ width: 24 }} />}
      >
        {handleLoggedIn()}
        
       {/* keeping for nested layout */}
        {/* <StyledTreeItem nodeId="3" labelText="Categories" labelIcon={Label}>
          <StyledTreeItem
            nodeId="5"
            labelText="Social"
            labelIcon={SupervisorAccountIcon}
            labelInfo="90"
            color="#1a73e8"
            bgColor="#e8f0fe"
          />
          <StyledTreeItem
            nodeId="6"
            labelText="Updates"
            labelIcon={InfoIcon}
            labelInfo="2,294"
            color="#e3742f"
            bgColor="#fcefe3"
          />
          <StyledTreeItem
            nodeId="7"
            labelText="Forums"
            labelIcon={ForumIcon}
            labelInfo="3,566"
            color="#a250f5"
            bgColor="#f3e8fd"
          />
          <StyledTreeItem
            nodeId="8"
            labelText="Promotions"
            labelIcon={LocalOfferIcon}
            labelInfo="733"
            color="#3c8039"
            bgColor="#e6f4ea"
          />
        </StyledTreeItem> */}
        
      </TreeView>

    </div>
  );
}
