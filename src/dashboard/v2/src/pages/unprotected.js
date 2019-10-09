import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles(theme => ({
  button: {
    margin: theme.spacing(1),
  },
  input: {
    display: 'none',
  },
}));

export default function Index() {
  const classes = useStyles();
  
  return (
    <div>  
      NOT PROTECTED
    </div>
  );
}