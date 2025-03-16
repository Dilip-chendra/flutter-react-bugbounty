import React from 'react';
import { Droppable } from 'react-beautiful-dnd';
import { Box, Typography } from '@mui/material';
import TaskCard from './TaskCard';
import { Task, TaskStage } from '../types/task';

interface KanbanColumnProps {
  stage: TaskStage;
  tasks: Task[];
  title: string;
}

const KanbanColumn: React.FC<KanbanColumnProps> = ({ stage, tasks, title }) => {
  return (
    <Box 
      sx={{ 
        width: '250px', 
        backgroundColor: '#e9ecef', 
        borderRadius: 2, 
        padding: 2,
        margin: 1 
      }}
    >
      <Typography variant="h5" sx={{ marginBottom: 2 }}>
        {title}
      </Typography>
      <Droppable droppableId={stage}>
        {(provided) => (
          <Box 
            ref={provided.innerRef} 
            {...provided.droppableProps}
            sx={{ minHeight: '400px' }}
          >
            {tasks.map((task, index) => (
              <TaskCard key={task.id} task={task} index={index} />
            ))}
            {provided.placeholder}
          </Box>
        )}
      </Droppable>
    </Box>
  );
};

export default KanbanColumn; 