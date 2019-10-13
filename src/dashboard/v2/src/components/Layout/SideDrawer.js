import React from 'react';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import Divider from '@material-ui/core/Divider';
import TreeView from '@material-ui/lab/TreeView';
import StyledTreeItem from './TreeItem'
import Link from "next/link";
import MyTheme from '../theme';
//icons
import DeleteIcon from '@material-ui/icons/Delete';
import SupervisorAccountIcon from '@material-ui/icons/SupervisorAccount';
import InfoIcon from '@material-ui/icons/Info';
import ForumIcon from '@material-ui/icons/Forum';
import LocalOfferIcon from '@material-ui/icons/LocalOffer';
import ArrowDropDownIcon from '@material-ui/icons/ArrowDropDown';
import ArrowRightIcon from '@material-ui/icons/ArrowRight';
//signin icon
import ExitToAppIcon from '@material-ui/icons/ExitToApp';
import LockIcon from '@material-ui/icons/Lock';
import ImageIcon from '@material-ui/icons/Image';



import Label from '@material-ui/icons/Label';

import Styles from '../Styles'
import Tab from '@material-ui/core/Tab';
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

  function show_login(){
    if(!hasUser){
      return (
        <Link href="/login">
          <StyledTreeItem color={MyTheme.palette.primary.main} nodeId="1" labelText="Signin" labelIcon={LockIcon} />
        </Link>
      )
    }
    else {
      return (
        <></>
      )
    }
  }

  function show_logout(){
    if(hasUser){
      return (
        <>
          <Link href="/auth/dashboardHome">
            <StyledTreeItem 
            bgColor={MyTheme.palette.blue500.color} 
            //textColor={MyTheme.palette.red500.color} 
            color='#FFFFFF'
            nodeId="1" labelText="Home" labelIcon={ImageIcon} />
          </Link>
          <Link href="/auth/tagImage">
            <StyledTreeItem 
            bgColor={MyTheme.palette.blue500.color} 
            //textColor={MyTheme.palette.red500.color} 
            color='#FFFFFF'
            nodeId="1" labelText="Tag Image" labelIcon={ImageIcon} />
          </Link>
          <Link href="/logout">
            <StyledTreeItem 
            bgColor={MyTheme.palette.red500.color} 
            //textColor={MyTheme.palette.red500.color} 
            color='#FFFFFF'
            nodeId="1" labelText="Logout" labelIcon={ExitToAppIcon} />
          </Link>
        </>
      )
    }
    else {
      return (
        <></>
      )
    }
  }

  const username= hasUser ? ','+props.user.nickname: '' 
  const role= hasUser ? ',': '' //props.user.userRole.data[0].name


  return (
    <div>
      <div className={classes.toolbar} />
      <Divider />
      <Tab label={"Welcome"+username+role} disableRipple/>
      <Divider />
      <TreeView
        className={classes.rootTree}
        defaultExpanded={['3']}
        defaultCollapseIcon={<ArrowDropDownIcon />}
        defaultExpandIcon={<ArrowRightIcon />}
        defaultEndIcon={<div style={{ width: 24 }} />}
      >
        {show_login()}
        {show_logout()}
       
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
