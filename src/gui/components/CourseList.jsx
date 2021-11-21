import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import Checkbox from '@mui/material/Checkbox';
import Avatar from '@mui/material/Avatar';

/**
 * Displays a list of courses
 * @param {courses} props 
 * @returns JSX
 */
export default function CourseList(props) {
    const {courses} = props;
    alert(courses.length); 
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
        {courses.map(function(courseName, i) {
          const labelId = `checkbox-list-secondary-label-${courseName}`;
          return (
            <ListItem
              key={courseName}
              disablePadding
            >
              <ListItemButton>
              <Checkbox
                  sx={{ marginRight: 3 }}
                  onChange={handleToggle(courseName)}
                  checked={checked.indexOf(courseName) !== -1}
                  inputProps={{ 'aria-labelledby': labelId }}
                />
                <ListItemAvatar>
                  <Avatar>{courseName}</Avatar>
                </ListItemAvatar>
                <ListItemText id={labelId} primary={courseName} />
              </ListItemButton>
            </ListItem>
          );
        })}
      </List>
    );
  }
