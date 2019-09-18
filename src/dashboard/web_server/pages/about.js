import React from 'react';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';
import MuiLink from '@material-ui/core/Link';
import Button from '@material-ui/core/Button';

import Link from '../components/Link';



export default function About() {
  return (
    <Container maxWidth="sm">
      <Box my={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          Next.js example
        </Typography>
        <Link>
        <Button variant="contained" color="primary"  href="/">
          Go to the main page
        </Button>
        </Link>
      
      </Box>
    </Container>
  );
}
