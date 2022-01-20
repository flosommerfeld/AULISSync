import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import Button from '@mui/material/Button';
import Avatar from '@mui/material/Avatar';
import {
  Link
} from "react-router-dom";

/**
 * Main bar of the application. DIsplays the apps name, current user and a logout button.
 * @param {username} props 
 * @returns 
 */
export default function MainAppBar(props) {
    const { username } = props;
  
    return (
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <IconButton
              size="large"
              edge="start"
              color="inherit"
              aria-label="menu"
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              AULISSync
            </Typography>
            <Button component={Link} to="/login" color="inherit">Logout</Button>
            <Avatar sx={{ marginLeft: 2}}>{username.substring(0,2)}</Avatar>
          </Toolbar>
        </AppBar>
      </Box>
    );
  }