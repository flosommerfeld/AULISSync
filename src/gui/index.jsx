import * as React from 'react';
import ReactDOM from 'react-dom';
import Button from '@mui/material/Button';

const App = function() {
  return <Button onClick={handleButton} variant="contained">Hello World</Button>;
}

function handleButton() {
  window.pywebview.api.handleButton()
}

const element = document.getElementById('app')
ReactDOM.render(<App />, element)
