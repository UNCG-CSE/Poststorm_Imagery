import React from 'react';

function DisplayImage(props) {
  const {imageName}=props
  return (
    <div>
      Look at: {imageName || 'error big sad'}

    </div>
  );
}



export default DisplayImage;
