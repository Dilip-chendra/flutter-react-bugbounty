import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Task, TaskStage } from '../types/task';
import { v4 as uuidv4 } from 'uuid';

interface TaskState {
  tasks: Task[];
  searchTerm: string;
}

const initialState: TaskState = {
  tasks: [],
  searchTerm: '',
};

const taskSlice = createSlice({
  name: 'tasks',
  initialState,
  reducers: {
    addTask: (state, action: PayloadAction<Omit<Task, 'id'>>) => {
      state.tasks.push({
        ...action.payload,
        id: uuidv4(),
      });
    },
    moveTask: (state, action: PayloadAction<{ taskId: string; newStage: TaskStage }>) => {
      const { taskId, newStage } = action.payload;
      const task = state.tasks.find(t => t.id === taskId);
      if (task) {
        task.stage = newStage;
      }
    },
    setSearchTerm: (state, action: PayloadAction<string>) => {
      state.searchTerm = action.payload;
    },
  },
});

export const { addTask, moveTask, setSearchTerm } = taskSlice.actions;
export default taskSlice.reducer; 