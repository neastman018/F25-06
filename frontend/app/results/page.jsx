'use client'
import * as React from 'react';
import {Box, CssBaseline, Toolbar} from '@mui/material';
import { Experimental_CssVarsProvider, experimental_extendTheme as extendTheme} from '@mui/material/styles';
import DrawerAppBar from '../components/navbar';
import Graphs from '../components/graphdisplay';
import SimsDrawer from '../components/simsdrawer';

const theme = extendTheme({
  colorSchemes: {
    light: {
      palette: {
        primary: {
          main: '#630031',
        },
      },
    },
    dark: {
      palette: {
        primary: {
          main: '#000',
        },
      },
    },
  },
  // ...other properties
});


const navItems = [
  {name:'Home', url:'.'}, 
  {name:'Project Info', url:'./project'},
  {name:'Approach', url:'./methodology'},
  {name:'About Us', url:'./aboutus'}
];

export default function ResultsPage() {


  return (
    <Experimental_CssVarsProvider theme={theme}>
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <DrawerAppBar navItems={navItems} theme={theme}/>
      <SimsDrawer />
      <Toolbar />
      <Graphs />
    </Box>

    
    </Experimental_CssVarsProvider>
  );
}
  