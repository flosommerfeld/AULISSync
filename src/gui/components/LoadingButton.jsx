import * as React from 'react';
import Button from '@mui/material/Button';
import CircularProgress from '@mui/material/CircularProgress';
import { blue } from '@mui/material/colors';

/**
 * Button that is able to display a circular loader when loading is true
 */
 export default function LoadingButton(props) {
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
