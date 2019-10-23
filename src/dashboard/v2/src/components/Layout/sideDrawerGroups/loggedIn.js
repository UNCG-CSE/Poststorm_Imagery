import React from 'react';
import StyledTreeItem from '../TreeItem'
import Link from "next/link";//'../../Link'
import MyTheme from '../../theme';
import Divider from '@material-ui/core/Divider';
//signin icon
import ExitToAppIcon from '@material-ui/icons/ExitToApp';

import ImageIcon from '@material-ui/icons/Image';

import HomeIcon from '@material-ui/icons/Home';


export default function notLoggedIn(props) {


  return (
    <div>
        {/* <Link href="/auth/dashboardHome">
          <StyledTreeItem 

          // myClickedBackgroundColor={MyTheme.palette.blue500.color} 
          // myHoverBackgroundColor={MyTheme.palette.red500.color} 
          // myTextColor='#00FF00'
          // myHoverTextColor='#0000FF'
          // myClickedTextColor='#FF0000'

          nodeId="1" labelText="Home" labelIcon={HomeIcon} />
        </Link> */}

        <Link href="/auth/tagImage">
          <StyledTreeItem 
        
          nodeId="1" labelText="Tag Image" labelIcon={ImageIcon} />
        </Link>

        <Divider />

        <Link href="/logout">
          <StyledTreeItem 
            myClickedBackgroundColor={MyTheme.palette.red500.color} 
            //myHoverBackgroundColor={MyTheme.palette.red500.color} 
            myTextColor={MyTheme.palette.red500.color} 
            myHoverTextColor={MyTheme.palette.red500.color} 
            myClickedTextColor={MyTheme.palette.grey100.color} 
          nodeId="1" labelText="Logout" labelIcon={ExitToAppIcon} />
        </Link>
    </div>
  );
}
