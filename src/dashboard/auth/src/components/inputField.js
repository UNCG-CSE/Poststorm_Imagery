
import React from 'react';
//for the inputs them self
import TextField from '@material-ui/core/TextField'
//theme
import MyTheme from '../theme';

//styling
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(theme => ({
    
    errorLabel:{
      color:MyTheme.palette.red500.color
    }
  }));

function shouldShowError(error){
    if(error===undefined)
    {
        return false
    }
    return true
}

function validatedInput(props) {
    const classes = useStyles();

    return (
        <>
            <TextField
            {...props}
            error={shouldShowError(props.errors)}
            />
           
                {props.errors && <div id={'feedback-'+props.id} className={classes.errorLabel}>{props.errors}</div>}
            
        </>
    );
}

// Link.propTypes = {
//   activeClassName: PropTypes.string,
//   as: PropTypes.string,
//   className: PropTypes.string,
//   href: PropTypes.string,
//   innerRef: PropTypes.oneOfType([PropTypes.func, PropTypes.object]),
//   naked: PropTypes.bool,
//   onClick: PropTypes.func,
//   prefetch: PropTypes.bool,
// };

export default validatedInput
