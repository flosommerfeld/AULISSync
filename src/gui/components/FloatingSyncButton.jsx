import * as React from 'react';
import Fab from '@mui/material/Fab';
import SyncIcon from '@mui/icons-material/Sync';


/**
 * FAB which handles the synchronization of the courses
 * @returns 
 */
export default function FloatingSyncButton() {
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

  /**
   * Calls the Python API to synchronize the courses. NOTE: the user must be logged in to do this
   */
export function handleSyncButton() {
    window.pywebview.api.synchronizeCourses();
}
