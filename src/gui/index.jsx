import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import ReactDOM from 'react-dom';
import Button from '@mui/material/Button';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import Checkbox from '@mui/material/Checkbox';
import Avatar from '@mui/material/Avatar';
import Grid from '@mui/material/Grid';
import ListItemIcon from '@mui/material/ListItemIcon';
import Fab from '@mui/material/Fab';
import Settings from '@mui/icons-material/Settings';
import SyncIcon from '@mui/icons-material/Sync';
import ClassIcon from '@mui/icons-material/Class';
import TextField from '@mui/material/TextField';
import CircularProgress from '@mui/material/CircularProgress';
import { blue } from '@mui/material/colors';
import {
  HashRouter as Router,
  Routes,
  Route,
  Link,
  useNavigate
} from "react-router-dom";
const App = function() {

  // Wait for pywebview to be ready before checking if the user is logged in
  window.addEventListener('pywebviewready', handleLoggedInUser);
  
  return (
    <Router>
      <Routes>
        <Route path="/login" caseSensitive={false} element={<Login />} />
        <Route path="/settings" caseSensitive={false} element={<Dashboard />} />
        <Route path="/" caseSensitive={false} element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export function handleLoggedInUser() {
  // Display the Dashboard if there is a logged in user
  window.pywebview.api.isUserLoggedIn().then((response) => {
    if(response){
      return <Dashboard /> 
    }
  });
}
export function handleLogout() {
  window.pywebview.api.logoutUser();
}

export function Login() {
  // logs out the user when visiting the login page
  window.pywebview.api.logoutUser();

  const [username, setUsername] = React.useState("");
  const [password, setPassword] = React.useState("");

  const onUsernameChange = (e) => setUsername(e.target.value);
  const onPasswordChange = (e) => setPassword(e.target.value);

  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(false);

  // history instance used for redirecting after a successful login
  const navigate = useNavigate();

  // use the python api to log in the user
  const handleSubmit = () => {
    setLoading(true);
    window.pywebview.api.loginUser(username, password).then((loginSuccess) => {
      // only redirect if the login was successful
      if(loginSuccess){
        navigate("/settings");
      }
      else{
        // activate the error state which will change the Textfields
        setError(true);
        // stop the loading animation
        setLoading(false);
      }
    });
  }

  return(
    <div style={{height: "100vh"}} >
      <Grid
        container
        spacing={0}
        direction="column"
        alignItems="center"
        justifyContent="center"
        style={{ minHeight: '100vh' }}
      >
        <Grid item xs={3} padding={3} alignItems="center">
          <Box
            sx={{
              marginTop: 8,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <Typography component="h1" variant="h5">
              Login with your AULIS/RZhsb account
            </Typography>
          </Box>
          <TextField
              error={error}
              onChange={onUsernameChange}
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="username"
              autoComplete="username"
              autoFocus
            />
            <TextField
              error={error}
              helperText={error ? "Please enter a correct username and password." : ""}
              onChange={onPasswordChange}
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
            />
            <LoadingButton
              onClick={handleSubmit}
              loading={loading}
              text="Login"
            />
        </Grid>      
      </Grid>
    </div>
  )
}

function LoadingButton(props) {
  const { onClick, loading, text } = props;
  return (
    <Button variant="contained" onClick={onClick} disabled={loading} type="submit"
      fullWidth
      variant="contained"
      sx={{ mt: 3, mb: 2 }}
    >
      {loading && <CircularProgress size={24} sx={{color: blue[500]}}/>}
      {!loading && text}
    </Button>
  );
}

export function Dashboard() {

  const [username, setUsername] = React.useState("");

  // Wait for pywebview to be ready before grabbing the username
  window.addEventListener('pywebviewready', getUsername);

  function getUsername() {
    window.pywebview.api.getUsername().then((response) => {
      setUsername(response);
    });
  }

  return (
    <div style={{height: "100vh"}} >
      <ButtonAppBar username={username}/>
      <Grid container spacing={0} height={'calc(100vh - 64px)'}>
          <Grid item xl={2} lg={2} md={4} xs={5} sx={{ borderRight: 1, borderRightColor: "rgba(0, 0, 0, 0.12)" }}>
            <MenuList />
          </Grid>
          <Grid item xl={10} lg={10} md={8} xs={7}>
            <CheckboxListSecondary></CheckboxListSecondary>
            <Button onClick={handleButton} variant="contained">Get list of courses</Button>
          </Grid>
          <FloatingSyncButton />
        </Grid>
      </div>
  )
}

export function handleButton() {
  window.pywebview.api.getCourses().then((response) => {
    // TODO fix this. Seems like it is not being executed
  });
}

export function FloatingSyncButton() {
  return (
      <Fab variant="extended" color="primary" aria-label="add" 
        sx={{
          position: "fixed",
          bottom: (theme) => theme.spacing(4),
          right: (theme) => theme.spacing(4)
        }}
        onClick={handleSyncButton}
      >
        <SyncIcon sx={{ mr: 1 }} />
        Synchronize
      </Fab>
  );
}

export function handleSyncButton() {
  window.pywebview.api.synchronizeCourses();
}

export default function ButtonAppBar(props) {
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



export function MenuList() {
  return (
    <Box sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}>
      <nav aria-label="main mailbox folders">
        <List>
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemIcon>
                <ClassIcon />
              </ListItemIcon>
              <ListItemText primary="All courses" />
            </ListItemButton>
          </ListItem>
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemIcon>
                <Settings />
              </ListItemIcon>
              <ListItemText primary="Settings" />
            </ListItemButton>
          </ListItem>
        </List>
      </nav>
    </Box>
  );
}


export function CheckboxListSecondary() {
  const [checked, setChecked] = React.useState([1]);

  const handleToggle = (value) => () => {
    const currentIndex = checked.indexOf(value);
    const newChecked = [...checked];

    if (currentIndex === -1) {
      newChecked.push(value);
    } else {
      newChecked.splice(currentIndex, 1);
    }

    setChecked(newChecked);
  };

  return (
    <List sx={{ width: '100%', bgcolor: 'background.paper' }}>
      {[0, 1, 2, 3].map((value) => {
        const labelId = `checkbox-list-secondary-label-${value}`;
        return (
          <ListItem
            key={value}
            disablePadding
          >
            <ListItemButton>
            <Checkbox
                sx={{ marginRight: 3 }}
                onChange={handleToggle(value)}
                checked={checked.indexOf(value) !== -1}
                inputProps={{ 'aria-labelledby': labelId }}
              />
              <ListItemAvatar>
                <Avatar
                  alt={`Avatar n°${value + 1}`}
                  src={`/static/images/avatar/${value + 1}.jpg`}
                />
              </ListItemAvatar>
              <ListItemText id={labelId} primary={`Line item ${value + 1}`} />
            </ListItemButton>
          </ListItem>
        );
      })}
    </List>
  );
}

const element = document.getElementById('app')
ReactDOM.render(<App />, element)
