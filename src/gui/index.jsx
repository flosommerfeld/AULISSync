import * as React from 'react';
import ReactDOM from 'react-dom';
import {
  HashRouter as Router,
  Routes,
  Route,
} from "react-router-dom";
import Dashboard from './components/Dashboard';
import Login from './components/Login';

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = React.useState(false); 

  function handleLoggedInUser() {
    // Ask the Python API if there is a logged in user
    window.pywebview.api.isUserLoggedIn().then((response) => {
      // Set state to true if the user is logged in
      if(response){
        setIsLoggedIn(true);
      }
    });
  }

  // Wait for pywebview to be ready before checking if the user is logged in
  window.addEventListener('pywebviewready', handleLoggedInUser);

  return (
    <Router>
      <Routes>
        <Route path="/login" caseSensitive={false} element={<Login />} />
        <Route path="/settings" caseSensitive={false} element={<Dashboard />} />
        { isLoggedIn ?
          <Route path="/" caseSensitive={false} element={<Dashboard isLoggedIn={isLoggedIn}/>} />
          :  
          <Route path="/" caseSensitive={false} element={<Login />} /> 
        }
      </Routes>
    </Router>
  );
}

const element = document.getElementById("app")
ReactDOM.render(<App />, element)
