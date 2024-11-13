'use client'
import * as React from 'react';
import {Box, CssBaseline, Toolbar} from '@mui/material';
import { Experimental_CssVarsProvider, experimental_extendTheme as extendTheme} from '@mui/material/styles';
import  AlgorithmTabs from '../components/tabs';
import DrawerAppBar from '../components/navbar';

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
  {name:'Results', url:'./results'},
  {name:'About Us', url:'./aboutus'}
];

export default function ApproachPage() {
  return (
    <Experimental_CssVarsProvider theme={theme}> 

      <Box sx={{ display: 'flex', p: 3, flexDirection: 'column'}}>
        <CssBaseline />
        <DrawerAppBar navItems={navItems} theme={theme}/>
        <Toolbar />
        <AlgorithmTabs />
      </Box>  
  
    </Experimental_CssVarsProvider>
  );
}

  