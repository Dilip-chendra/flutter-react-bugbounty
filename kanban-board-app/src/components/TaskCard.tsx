import React from 'react';
import { Draggable } from 'react-beautiful-dnd';
import { Card, CardContent, Typography } from '@mui/material';
import { Task } from '../types/task';

interface TaskCardProps {
  task: Task;
  index: number;
}

const TaskCard: React.FC<TaskCardProps> = ({ task, index }) => {
  return (
    <Draggable draggableId={task.id} index={index}>
      {(provided) => (
        <Card 
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          sx={{ 
            marginBottom: 2, 
            backgroundColor: '#f4f4f4',
            boxShadow: 1 
          }}
        >
          <CardContent>
            <Typography variant="h6" sx={{ fontSize: 16 }}>
              {task.title}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {task.description.length > 100 
                ? `${task.description.slice(0, 100)}...` 
                : task.description}
            </Typography>
          </CardContent>
        </Card>
      )}
    </Draggable>
  );
};

export default TaskCard; 