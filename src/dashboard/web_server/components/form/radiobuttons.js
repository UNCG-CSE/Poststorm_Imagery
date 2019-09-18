/* eslint-disable jsx-a11y/anchor-has-content */
import React from 'react';
import MyTheme from "../theme";
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';
import { makeStyles, withStyles  } from "@material-ui/core/styles";

import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';



const useStyles = makeStyles(theme => ({
  //https://codesandbox.io/s/material-ui-both-right-and-left-aligned-icons-in-appbar-2e5qr

  formControl: {
    margin: theme.spacing(3),
  },
 
}));
function CheckboxForm(props) {
  const classes = useStyles();
  //radio buttons
  const [devTypeValue, setDevTypeValue] = React.useState({
    Developed: false,
    Undevelopd: false,
  });
  const [washoverValue, setWashoverValue] = React.useState({
    VisableWashover: false,
    NoVisableWashover: false,
  });
  const [IDKVALUE, setIDKVALUE] = React.useState({
    Swash: false,
    Collision: false,
    Inundation: false,
    Overwash: false,
  });
  const [radio_box_values,set_radio_values]=React.useState({
    devType:{
      Developed: false,
      Undevelopd: false,
    },
    washoverValue:{
      VisableWashover: false,
      NoVisableWashover: false,
    },
    idkvalue:{
      Swash: false,
      Collision: false,
      Inundation: false,
      Overwash: false,
    }
  });

  function handleChange(fnc,event) {
    //fnc(event.target.value);
    set_radio_values({
      ...radio_box_values,
      [fnc]:{
        ...radio_box_values.fnc,
        [event.target.value]:true
      }
    })
  }


  return (
    <FormControl  component="fieldset" className={classes.formControl}>
      <FormLabel component="legend" style={MyTheme.palette.amber500}>Development type</FormLabel>
      <RadioGroup aria-label="DevType"  name="DevType" value={Object.keys(radio_box_values.devType)[0]} onChange={(e) => handleChange('devType', e)} row>
          <FormControlLabel value="Developed" control={<Radio style={MyTheme.palette.amber500} />} label="Developed"  />
          <FormControlLabel  value="Undevelopd" control={<Radio style={MyTheme.palette.amber500} />} label="Undevelopd" />
      </RadioGroup>

      <br/>
      
      <FormLabel component="legend" style={MyTheme.palette.blue500}>Washover type</FormLabel>
      <RadioGroup aria-label="WashoverType" name="WashoverType" value={Object.keys(radio_box_values.washoverValue)[0]} onChange={(e) => handleChange('washoverValue', e)} row>
          <FormControlLabel value="VisableWashover" control={<Radio style={MyTheme.palette.blue500} />} label="Visable Washover"  />
          <FormControlLabel value="NoVisableWashover" control={<Radio style={MyTheme.palette.blue500} />} label="No Visable Washover" />
      </RadioGroup>
      <br/>

      <FormLabel component="legend" style={MyTheme.palette.green500}>IDK WHAT TO CALL THIS</FormLabel>
      <RadioGroup aria-label="IDKWATTHISIS" name="IDKWATTHISIS" value={Object.keys(radio_box_values.idkvalue)[0]} onChange={(e) => handleChange('idkvalue', e)} row>
          <FormControlLabel value="Swash" control={<Radio style={MyTheme.palette.green500} />} label="Swash"  />
          <FormControlLabel value="Collision" control={<Radio style={MyTheme.palette.green500} />} label="Collision" />
          <FormControlLabel value="Inundation" control={<Radio style={MyTheme.palette.green500} />} label="Inundation"  />
          <FormControlLabel value="Overwash" control={<Radio style={MyTheme.palette.green500} />} label="Overwash" />
      </RadioGroup>
    </FormControl>
  );
}



export default CheckboxForm;
