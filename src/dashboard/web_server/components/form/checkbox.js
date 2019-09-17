/* eslint-disable jsx-a11y/anchor-has-content */
import React from 'react';
import MyTheme from "../../src/theme";
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';


import FormGroup from '@material-ui/core/FormGroup';
import Checkbox from '@material-ui/core/Checkbox';
import { makeStyles, withStyles  } from "@material-ui/core/styles";


const useStyles = makeStyles(theme => ({
  //https://codesandbox.io/s/material-ui-both-right-and-left-aligned-icons-in-appbar-2e5qr

  formControl: {
    margin: theme.spacing(2,0,0,3),
  },
 
}));
function CheckboxForm(props) {
  const classes = useStyles();
  //check boxes
  const [checkbox_state, setState_checkbox] = React.useState({
    Marsh: false,
    River: false,
    SandyCoastline: false,
  });

  const { Marsh, River, SandyCoastline } = checkbox_state;

  const handleChange_checkbox = name => event => {
    setState_checkbox({ ...checkbox_state, [name]: event.target.checked });
  };


  return (
    <FormControl component="fieldset" className={classes.formControl}>
      <FormLabel component="legend" style={MyTheme.palette.purple500}>Land Type</FormLabel>
      <FormGroup  row>
          <FormControlLabel
          control={<Checkbox checked={River} onChange={handleChange_checkbox('River')} value="River" style={MyTheme.palette.purple500} />}
          label="River" 
          />
          <FormControlLabel
          control={<Checkbox checked={Marsh} onChange={handleChange_checkbox('Marsh')} value="Marsh" style={MyTheme.palette.purple500}/>}
          label="Marsh" 
          />
          <FormControlLabel
          control={
              <Checkbox checked={SandyCoastline} onChange={handleChange_checkbox('SandyCoastline')} value="Sandy Coastline" style={MyTheme.palette.purple500}/>
          }
          label="Sandy Coastline" 
          />
      </FormGroup>
    </FormControl>
  );
}



export default CheckboxForm;
