<AppBar position="static">
<Tabs value={value} onChange={handleChange} aria-label="simple tabs example">
  {/* <Tab label="Pick a storm" {...a11yProps(0)} /> */}
  <Tab label="Tag Image" {...a11yProps(1)} />
 
</Tabs>
</AppBar>
<TabPanel value={value} index={-1}>
<Formik
  initialValues={{
    stormId: -1
  }}
  validationSchema={Yup.object().shape({
    stormId: Yup.number().positive('Please select a option').required("Please select a option"),
  })}
  onSubmit={async (values )=> {
    console.log(values,IP)
    // const response = await fetch(`http://${IP}:3000/api/stormToTag`, {
    //   method: 'POST', // *GET, POST, PUT, DELETE, etc.
    //   mode: 'cors', // no-cors, *cors, same-origin
    //   cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    //   credentials: 'same-origin', // include, *same-origin, omit
    //   headers: {
    //     'Content-Type': 'application/json'
    //     // 'Content-Type': 'application/x-www-form-urlencoded',
    //   },
    //   redirect: 'follow', // manual, *follow, error
    //   referrer: 'no-referrer', // no-referrer, *client
    //   body: JSON.stringify(values) // body data type must match "Content-Type" header
    // });
    // await response.json(); 
    handleChange(1)
    axios.post(`http://${IP}:3000/api/stormToTag`, values)
    .then(res => {
      console.log(res);
      console.log(res.data);
    })
  }}
  render={propsFormik => (
    <Form>
    
      <Field
        required
        name="stormId"
        label="Storm"
        options={[
          ...props.initProps.storms
        ]}
        component={Select}
        error={propsFormik.errors.stormId !== undefined}
      />
      { propsFormik.errors.stormId &&
        (<div style={MyTheme.palette.red500}>
          {propsFormik.errors.stormId}
        </div>)
      }
      {/* <button
        type="submit"
        disabled={propsFormik.values.stormId==-1}
      >
        Submit
      </button> */}

      <Button 
      variant="contained"
      type="submit"
      color="primary"
      disabled={propsFormik.values.stormId==-1}
      >
        Default
      </Button>
      
    </Form>
  )}
/>
</TabPanel>
<TabPanel value={value} index={0} >
<DisplayImage/>
</TabPanel>