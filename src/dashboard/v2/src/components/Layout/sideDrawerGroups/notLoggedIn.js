import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import StyledTreeItem from './../TreeItem'
import Link from "next/link";
//icons
//signin icon
import LockIcon from '@material-ui/icons/Lock';

import Styles from '../../Styles'


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
