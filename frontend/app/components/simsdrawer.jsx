import * as React from 'react';
import { styled, useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import CssBaseline from '@mui/material/CssBaseline';
import MuiAppBar from '@mui/material/AppBar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import Button from '@mui/material/Button';
import WestIcon from '@mui/icons-material/West';
import MenuOpenIcon from '@mui/icons-material/MenuOpen';
import DeleteIcon from '@mui/icons-material/Delete';
import UploadIcon from '@mui/icons-material/Upload';
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css'
import DragNDrop from './uploadpopup';
import TextField from '@mui/material/TextField';
import SearchIcon from '@mui/icons-material/Search';
import { useSearch } from '../hooks/get_search';
import CircularProgress from '@mui/material/CircularProgress';
import SimPopUp from './simpopup';

const drawerWidth = 300;

const Main = styled('main', { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme }) => ({
    flexGrow: 1,
    padding: theme.spacing(3),
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    marginLeft: `-${drawerWidth}px`,
    variants: [
      {
        props: ({ open }) => open,
        style: {
          transition: theme.transitions.create('margin', {
            easing: theme.transitions.easing.easeOut,
            duration: theme.transitions.duration.enteringScreen,
          }),
          marginLeft: 0,
        },
      },
    ],
  }),
);

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ theme }) => ({
  transition: theme.transitions.create(['margin', 'width'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  variants: [
    {
      props: ({ open }) => open,
      style: {
        width: `calc(100% - ${drawerWidth}px)`,
        marginLeft: `${drawerWidth}px`,
        transition: theme.transitions.create(['margin', 'width'], {
          easing: theme.transitions.easing.easeOut,
          duration: theme.transitions.duration.enteringScreen,
        }),
      },
    },
  ],
}));

const DrawerHeader = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
  justifyContent: 'flex-end',
}));




export default function PersistentDrawerLeft() {
  const theme = useTheme();
  const [open, setOpen] = React.useState(false);
  const [files, setFiles] = React.useState([]);

  const [search, setSearch] = React.useState("");
  const [deleteFile, setDeleteFile] = React.useState(-1);

  const { data: search_results, isLoading, isError } = useSearch(search, deleteFile);


  const handleSearch = (event) => {
    console.log(event.target.value);
    setSearch(event.target.value); // Set the search value on pressing Enter
  };

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  const handleClearClick = () => {
    if (window.confirm('Do you want to delete all the Simulation Logs')) {
      const password = prompt('Please enter the password to clear logs:');
      if (password === 'ClearLogs') {
        setDeleteFile(-10)
        alert('All logs have been cleared');
      } else {
        alert('Incorrect password. Logs have not been cleared.');
      }
    }
  };

  


  const [showDragNDrop, setShowDragNDrop] = React.useState(false);
  const [showSimLog, setShowSimLog] = React.useState(false);

  const handleUploadClick = () => {
    setShowDragNDrop(!showDragNDrop);
  };

  const handleSimLogClick = () => {
    setShowSimLog(!showSimLog);
  };

  const handleDeleteFile = (index) => {
    if (window.confirm('Do you want to delete this Simulation Logs')) {
      setDeleteFile(index),
      console.log(index),
      console.log(typeof index)
    }
  }

  React.useEffect(() => {
    setDeleteFile(-1);
  }, [search_results]);

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <Box sx={{ position: 'absolute', paddingTop: '85px', paddingLeft: '15px' }}>
        <Button
          variant="contained"
          aria-label="open drawer"
          onClick={handleDrawerOpen}
          edge="start"
          sx={{
            mr: 2,
            height: '40px',
            display: 'flex',
            alignItems: 'center', // Align icon and text vertically
            justifyContent: 'center', // Ensure content is centered
            whiteSpace: 'nowrap', // Prevent text wrapping
            border: '2px solid darkgrey', // Dark grey border
            backgroundColor: 'lightgrey', // Light grey fill
            color: 'black', // Text color
            textTransform: 'none', // Prevent text from being all caps
            '&:hover': {
              backgroundColor: 'grey', // Slightly darker grey on hover
            },
          }}
        >
          <MenuOpenIcon sx={{ marginRight: '8px', color: 'black' }} /> {/* Icon color to match text */}
          <Typography sx={{ fontSize: '12px' }}>Show Simulation Logs</Typography>
        </Button>
      </Box>

      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
        variant="persistent"
        anchor="left"
        open={open}
      >
        <DrawerHeader />
        <ListItemIcon
          onClick={handleDrawerClose}
          sx={{ height: '40px', minHeight: '40px', padding: '16px', justifyContent: 'flex-end', alignContent: 'center' }}
        >
          <Typography sx={{ color: 'grey', fontWeight: 'bold', fontSize: '16px' }}>
            <WestIcon />
          </Typography>
        </ListItemIcon>
        <Divider />
        <List>
          <ListItemButton onClick={handleClearClick}>
            <DeleteIcon sx={{ marginRight: '16px' }} /> {/* Add margin to create indent */}
            <Typography>Clear Logs</Typography>
          </ListItemButton>
          <ListItemButton onClick={handleUploadClick}>
            <UploadIcon sx={{ marginRight: '16px' }} /> {/* Add margin to create indent */}
            <Typography>Upload Logs</Typography>
          </ListItemButton>
          <Popup
            open={showDragNDrop}
            onClose={() => setShowDragNDrop(false)}
            modal
            closeOnDocumentClick
            contentStyle={{
              maxHeight: "50vh", // Set the maximum height of the popup
              overflowY: "auto", // Allow vertical scrolling if content exceeds max height
            }}
          >
            <DragNDrop onFilesSelected={setFiles} />
          </Popup>

        </List>
        <Divider />
        <Box sx={{ display: 'flex', alignItems: 'center', paddingLeft: '5px' }}>
          <Button onClick={() => {
              const inputValue = document.getElementById('standard-basic').value;
              setSearch(inputValue); //Set search value when clicking the button
              console.log(inputValue);
            }}>
              <SearchIcon sx={{ marginRight: '8px' }} />
          </Button>
          <TextField
            id="standard-basic"
            label="Search"
            variant="standard"
            onKeyDown={(event) => {
              if (event.key === 'Enter') {
                handleSearch(event);
              }
            }}
          />
        </Box>
        <Divider />

       
        {isLoading ? (
            <CircularProgress />
        ) : isError ? (
            <Typography color="error">Error Getting Files</Typography>
        ) : search_results?.json_files ? (
          <Box>
            {search_results.file_names.map((fileName, index) => (
              <Box key={index} sx={{ display: 'flex', alignItems: 'center', marginBottom: '8px' }}>
                <Button
                  onClick={() => handleDeleteFile(index)}
                  sx={{ minWidth: 'auto', paddingLeft: '16px' }}
                >
                  <DeleteIcon sx={{ marginRight: '16px' }} />
                </Button>
                <ListItemButton onClick={handleSimLogClick} sx={{ flexGrow: 1 }}>
                  <Typography>{fileName}</Typography>
                </ListItemButton>
                <Popup open={showSimLog} onClose={() => setShowSimLog(false)} modal>
                  <SimPopUp code={search_results.json_files[index]} />
                </Popup>
              </Box>
            ))}
          </Box>
        ) : (
          <Typography>No Search Results</Typography>
        )}
      </Drawer>
      <Main open={open}></Main>
    </Box>
  );
}