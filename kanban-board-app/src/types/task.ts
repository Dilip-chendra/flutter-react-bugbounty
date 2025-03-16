export interface Task {
  id: string;
  title: string;
  description: string;
  stage: 'todo' | 'inProgress' | 'peerReview' | 'done';
}

export type TaskStage = Task['stage']; 