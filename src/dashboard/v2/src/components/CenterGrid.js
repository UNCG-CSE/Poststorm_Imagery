import React from 'react';
import Grid from '@material-ui/core/Grid';

;

function CenterGrid(props) {
  return (
    <div>
      <Grid
          container
          direction="column"
          justify="center"
          alignItems="center"
      >
        {props.children}
      </Grid>

    </div>
  );
}



export default CenterGrid;
