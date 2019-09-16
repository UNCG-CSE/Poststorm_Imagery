import { 
  red,
  purple,
  blue,
  orange,
  yellow,
  green,
  cyan,
  teal,
  amber
} from '@material-ui/core/colors';
import { createMuiTheme } from '@material-ui/core/styles';

// A custom theme for this app
const theme = createMuiTheme({
  palette: {
    type: 'dark',
    primary: {
      main: '#556cd6',
    },
    secondary: {
      main: '#19857b',
    },
    error: {
      main: red.A400,
    },

    //300
    teal300: {
      color: teal[300]
    },
    teal300BG: {
      backgroundColor: teal[300]
    },
    purple300: {
      color: purple[300]
    },

    //400
    blue400: { 
        color: blue[400]
    },
    blue400BG: { 
      backgroundColor: blue[400]
  },
    purple400: {
      color: purple[400]
    },

    //500
    red500: {
      color: red[500]
    },
    blue500: {
      color: blue[500]
    },
    orange500: {
      color: orange[500]
    },
    yellow500: {
      color: yellow[500]
    },
    green500: {
      color: green[500]
    },
    cyan500: {
      color: cyan[500]
    },
    cyan500BG: {
      backgroundColor: cyan[500]
    },
    purple500: {
      color: purple[500]
    },
    purple500BG: {
      backgroundColor: purple[500]
    },
    amber500: {
      color: amber[500]
    },
    amber500BG: {
      backgroundColor: amber[500]
    },

    //600
    blueBG600: { 
      backgroundColor: blue[600]
    },

    //700
    yellow700: {
      color: yellow['A200']
    },

    //800
    cyan800BG: {
      backgroundColor: cyan['800']
    }
    
  },
});
//https://stackoverflow.com/questions/50069724/how-to-add-multiple-material-ui-palette-colors custom colors
export default theme;
