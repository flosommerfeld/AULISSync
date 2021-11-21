import * as React from 'react';
import Grid from '@mui/material/Grid';
import MenuList from './MenuList';
import CourseList from './CourseList';
import MainAppBar from './MainAppBar';
import FloatingSyncButton from './FloatingSyncButton';

/**
 * The dashboard is the view a user sees when he logs into the app.
 * It shows a AppBar on top, MenuList on the left and a CourseList in the middle.
 * @param {*} props 
 * @returns 
 */
export default function Dashboard(props) {
    const {isLoggedIn} = props;
  
    const [username, setUsername] = React.useState("");
    const [courses, setCourses] = React.useState([]);
  
    // get Data from Python API
    React.useEffect(()=>{
      if(isLoggedIn){
        getData();
      }
    }, []); // do only once
  
    /**
     * Gets the needed data (login status, courses, username) by calling the Python API
     */
    function getData() {
      alert("READY");
      // 1. Verify that the user is logged into AULIS
      window.pywebview.api.isUserLoggedIntoAulis().then((loggedIn) => {
        if(!loggedIn){
          alert("not logged in Selenium AULIS");
          return window.pywebview.api.loginAuthenticatedUserToAulis();
        }
      // 2. Grab all of the AULIS courses which are shown on the AULIS website 
      }).then(() => { 
        alert("trying to get courses");
        window.pywebview.api.getCourses().then((response) => {
          response.forEach((item) => { item = String(item) })
          document.getElementById("demo").innerHTML = response;
          
          setCourses(response); // TODO: fix this! somehow throws an error
          
        }).catch((response) => {alert(response);} );
      });
  
      // Get the username
      window.pywebview.api.getUsername().then((response) => {
        setUsername(response);
      });
  
    }
  
    return (
      <div style={{height: "100vh"}} >
        <MainAppBar username={username}/>
        <Grid container spacing={0} height={'calc(100vh - 64px)'}>
            <Grid item xl={2} lg={2} md={4} xs={5} sx={{ borderRight: 1, borderRightColor: "rgba(0, 0, 0, 0.12)" }}>
              <MenuList />
            </Grid>
            <Grid item xl={10} lg={10} md={8} xs={7}>
              <CourseList courses={courses} />
            </Grid>
            <FloatingSyncButton />
          </Grid>
        </div>
    )
  }
