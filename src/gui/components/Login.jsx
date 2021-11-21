import * as React from 'react';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import { Typography } from '@mui/material';
import {
  useNavigate
} from "react-router-dom";
import LoadingButton from './LoadingButton';

/**
 * This is the login view.
 * @returns 
 */
export default function Login() {
    // logs out the user when visiting the login page
    // TODO window.pywebview.api.logoutUser();
  
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
  