import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import PropTypes from 'prop-types';
import TreeItem from '@material-ui/lab/TreeItem';
import red from '@material-ui/core/colors/red';
import MyTheme from '../theme';

const useTreeItemStyles = makeStyles(theme => ({
    root: {
      color: theme.palette.text.primary,
      '&:focus > $content': {
        backgroundColor: `var(--tree-view-clicked-backgroundcolor, ${theme.palette.grey[700]})`,
        color: `var(--tree-view-clicked-textcolor,${MyTheme.palette.primary.main})`,
        bordeRradius: '110px'
      },
    },
    content: {
      //text color
      color: `var(--tree-view-textcolor, ${theme.palette.grey[100]})`,
      paddingRight: theme.spacing(1),
      fontWeight: theme.typography.fontWeightMedium,
      '$expanded > &': {
        fontWeight: theme.typography.fontWeightRegular,
      },
      //hover effect
      '&:hover': {
        color:`var(--tree-view-hover-textcolor, ${theme.palette.grey[100]})`,
        backgroundColor:`var(--tree-view-hover-backgroundcolor, ${MyTheme.palette.primary.main})`//`${MyTheme.palette.primary.main}`,
      },
    },
    group: {
      marginLeft: 0,
      '& $content': {
        paddingLeft: theme.spacing(2),
      },
    },
    expanded: {},
    label: {
      fontWeight: 'inherit',
      color: 'inherit',
    },
    labelRoot: {
      display: 'flex',
      alignItems: 'center',
      padding: theme.spacing(0.5, 0),
    },
    labelIcon: {
      marginRight: theme.spacing(1),
    },
    labelText: {
      fontWeight: 'inherit',
      flexGrow: 1,
    },
  }));

StyledTreeItem.propTypes = {
    bgColor: PropTypes.string,
    color: PropTypes.string,
    labelIcon: PropTypes.elementType.isRequired,
    labelInfo: PropTypes.string,
    labelText: PropTypes.string.isRequired,
};

function StyledTreeItem(props) {
    const classes = useTreeItemStyles();
    const { 
      labelText,textColor, 
      labelIcon: LabelIcon, 
      labelInfo, 
      color, 
      bgColor,
      myClickedBackgroundColor,
      myHoverBackgroundColor,
      myTextColor,
      myHoverTextColor,
      myClickedTextColor,
      ...other 
    } = props;
  
    return (
      <TreeItem
        label={
          <div className={classes.labelRoot}>
            <LabelIcon color="inherit" className={classes.labelIcon} />
            <Typography variant="body2" className={classes.labelText}
              style={{
                'color':textColor
              }}
            >
              {labelText}
            </Typography>
            <Typography variant="caption" color="inherit">
              {labelInfo}
              
            </Typography>
          </div>
        }
        style={{
          // '--tree-view-color': color,
          // '--tree-view-bg-color': bgColor,

          '--tree-view-textcolor': myTextColor,
          '--tree-view-clicked-textcolor': myClickedTextColor,
          '--tree-view-hover-textcolor': myHoverTextColor,
          '--tree-view-hover-backgroundcolor': myHoverBackgroundColor,
          '--tree-view-clicked-backgroundcolor': myClickedBackgroundColor,
        }}
        classes={{
          root: classes.root,
          content: classes.content,
          expanded: classes.expanded,
          group: classes.group,
          label: classes.label,
        }}
        {...other}
      />
    );
  }

export default React.forwardRef((props,ref) => <StyledTreeItem {...props} innerRef={ref}  />);



