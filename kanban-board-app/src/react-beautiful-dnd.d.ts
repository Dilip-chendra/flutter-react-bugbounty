import { ReactNode } from 'react';

declare module 'react-beautiful-dnd' {
  export interface DraggableProvided {
    innerRef: (element: HTMLElement | null) => void;
    draggableProps: {
      style?: React.CSSProperties;
      'data-rbd-draggable-context-id'?: string;
      'data-rbd-draggable-id'?: string;
    };
    dragHandleProps?: {
      onMouseDown: (event: MouseEvent) => void;
      onKeyDown: (event: KeyboardEvent) => void;
    } | null;
  }

  export interface DroppableProvided {
    innerRef: (element: HTMLElement | null) => void;
    droppableProps: {
      'data-rbd-droppable-context-id'?: string;
      'data-rbd-droppable-id'?: string;
    };
    placeholder?: ReactNode;
  }

  export interface DropResult {
    draggableId: string;
    type: string;
    source: {
      index: number;
      droppableId: string;
    };
    destination?: {
      droppableId: string;
      index: number;
    } | null;
  }

  export function Draggable(props: {
    draggableId: string;
    index: number;
    children: (provided: DraggableProvided, snapshot: any) => ReactNode;
  }): ReactNode;

  export function Droppable(props: {
    droppableId: string;
    children: (provided: DroppableProvided, snapshot: any) => ReactNode;
  }): ReactNode;

  export function DragDropContext(props: {
    onDragEnd: (result: DropResult) => void;
    children: ReactNode;
  }): ReactNode;
} 