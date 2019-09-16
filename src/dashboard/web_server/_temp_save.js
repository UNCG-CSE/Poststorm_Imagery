<form className="commentForm" onSubmit={handleSubmit}>
  
         
        


<FormControl  component="fieldset" className={classes.formControl}>
<FormLabel component="legend" style={MyTheme.palette.amber500}>Development type</FormLabel>
<RadioGroup aria-label="DevType"  name="DevType" value={Object.keys(radio_box_values.devType)[0]} onChange={(e) => handleChange('devType', e)} row>
    <FormControlLabel value="Developed" control={<Radio style={MyTheme.palette.amber500} />} label="Developed"  />
    <FormControlLabel  value="Undevelopd" control={<Radio style={MyTheme.palette.amber500} />} label="Undevelopd" />
</RadioGroup>
</FormControl>

<br/>


        
<br/>

<FormControl component="fieldset" className={classes.formControl}>
<FormLabel component="legend" style={MyTheme.palette.blue500}>Washover type</FormLabel>
<RadioGroup aria-label="WashoverType" name="WashoverType" value={Object.keys(radio_box_values.washoverValue)[0]} onChange={(e) => handleChange('washoverValue', e)} row>
    <FormControlLabel value="VisableWashover" control={<Radio style={MyTheme.palette.blue500} />} label="Visable Washover"  />
    <FormControlLabel value="NoVisableWashover" control={<Radio style={MyTheme.palette.blue500} />} label="No Visable Washover" />
</RadioGroup>
</FormControl>

<br/>

<FormControl component="fieldset" className={classes.formControl}>
<FormLabel component="legend" style={MyTheme.palette.green500}>IDK WHAT TO CALL THIS</FormLabel>
<RadioGroup aria-label="IDKWATTHISIS" name="IDKWATTHISIS" value={Object.keys(radio_box_values.idkvalue)[0]} onChange={(e) => handleChange('idkvalue', e)} row>
    <FormControlLabel value="Swash" control={<Radio style={MyTheme.palette.green500} />} label="Swash"  />
    <FormControlLabel value="Collision" control={<Radio style={MyTheme.palette.green500} />} label="Collision" />
    <FormControlLabel value="Inundation" control={<Radio style={MyTheme.palette.green500} />} label="Inundation"  />
    <FormControlLabel value="Overwash" control={<Radio style={MyTheme.palette.green500} />} label="Overwash" />
</RadioGroup>
</FormControl>
           
<CardActions style={MyTheme.palette.bluePrimaryBG}>
{/* <Button size="small" variant="contained" color="inherit" style={MyTheme.palette.red500}>
    Skip
</Button> */}
       
<SkipButton size="small" variant="contained" color="primary" className={classes.margin}>
    Skip
</SkipButton>
<SubmitButton  size="small" variant="contained" color="primary" className={classes.toolbarButtons} type="submit">
    Submit
</SubmitButton>
{/* <Button type="submit" size="small" variant="contained" color="primary" className={classes.toolbarButtons} type="submit">
    Primary
</Button> */}
</CardActions>
</form> 