import * as React from 'react';
import ReactDOM from 'react-dom';
import Button from '@mui/material/Button';

const App = function() {
  return <Button variant="contained">Hello World</Button>;
}

const element = document.getElementById('app')
ReactDOM.render(<App />, element)
