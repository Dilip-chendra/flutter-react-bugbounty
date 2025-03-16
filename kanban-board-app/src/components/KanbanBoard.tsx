import React, { useState } from 'react';
import { DragDropContext, DropResult } from 'react-beautiful-dnd';
import { 
  Box, 
  TextField, 
  Button, 
  Dialog, 
  DialogTitle, 
  DialogContent, 
  DialogActions 
} from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import KanbanColumn from './KanbanColumn';
import { RootState } from '../redux/store';
import { moveTask, addTask, setSearchTerm } from '../redux/taskSlice';
import { Task, TaskStage } from '../types/task';

const KanbanBoard: React.FC = () => {
  const dispatch = useDispatch();
  const { tasks, searchTerm } = useSelector((state: RootState) => state.tasks);
  const [isAddTaskOpen, setIsAddTaskOpen] = useState(false);
  const [newTask, setNewTask] = useState<Omit<Task, 'id'>>({
    title: '',
    description: '',
    stage: 'todo'
  });

  const handleDragEnd = (result: DropResult) => {
    const { source, destination } = result;
    if (!destination) return;

    dispatch(moveTask({
      taskId: result.draggableId,
      newStage: destination.droppableId as TaskStage
    }));
  };

  const handleAddTask = () => {
    dispatch(addTask(newTask));
    setIsAddTaskOpen(false);
    setNewTask({ title: '', description: '', stage: 'todo' });
  };

  const filteredTasks = tasks.filter(task => 
    task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    task.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const columnData = [
    { 
      stage: 'todo' as TaskStage, 
      title: 'To Do', 
      tasks: filteredTasks.filter(t => t.stage === 'todo') 
    },
    { 
      stage: 'inProgress' as TaskStage, 
      title: 'In Progress', 
      tasks: filteredTasks.filter(t => t.stage === 'inProgress') 
    },
    { 
      stage: 'peerReview' as TaskStage, 
      title: 'Peer Review', 
      tasks: filteredTasks.filter(t => t.stage === 'peerReview') 
    },
    { 
      stage: 'done' as TaskStage, 
      title: 'Done', 
      tasks: filteredTasks.filter(t => t.stage === 'done') 
    }
  ];

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', padding: 2 }}>
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        marginBottom: 2 
      }}>
        <TextField
          label="Search Tasks"
          variant="outlined"
          fullWidth
          value={searchTerm}
          onChange={(e) => dispatch(setSearchTerm(e.target.value))}
          sx={{ marginRight: 2 }}
        />
        <Button 
          variant="contained" 
          color="primary"
          onClick={() => setIsAddTaskOpen(true)}
        >
          Add Task
        </Button>
      </Box>

      <DragDropContext onDragEnd={handleDragEnd}>
        <Box sx={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          overflowX: 'auto' 
        }}>
          {columnData.map(column => (
            <KanbanColumn 
              key={column.stage}
              stage={column.stage}
              title={column.title}
              tasks={column.tasks}
            />
          ))}
        </Box>
      </DragDropContext>

      <Dialog 
        open={isAddTaskOpen} 
        onClose={() => setIsAddTaskOpen(false)}
      >
        <DialogTitle>Add New Task</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Task Title"
            fullWidth
            value={newTask.title}
            onChange={(e) => setNewTask(prev => ({ ...prev, title: e.target.value }))}
          />
          <TextField
            margin="dense"
            label="Task Description"
            fullWidth
            multiline
            rows={4}
            value={newTask.description}
            onChange={(e) => setNewTask(prev => ({ ...prev, description: e.target.value }))}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setIsAddTaskOpen(false)}>Cancel</Button>
          <Button 
            onClick={handleAddTask} 
            disabled={!newTask.title || !newTask.description}
          >
            Add Task
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default KanbanBoard; 