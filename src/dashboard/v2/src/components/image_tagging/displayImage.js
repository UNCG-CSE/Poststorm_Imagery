import React, { useState } from 'react';


import Grid from '@material-ui/core/Grid';

function DisplayImage(props) {
  const {imageName}=props
  return (
    <div> 
      Look at: {imageName || 'error big sad'}
     
    </div>
  );
}



export default DisplayImage;