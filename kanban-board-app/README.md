# Kanban Board Application

## Overview
This is a Kanban Board application built with React, Redux, and Material-UI. It allows users to manage tasks across different stages: To Do, In Progress, Peer Review, and Done.

## Features
- Drag and drop task management
- Search functionality to filter tasks
- Add new tasks with title and description
- Responsive design
- State management with Redux

## Prerequisites
- Node.js (v14 or later)
- npm (v6 or later)

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/kanban-board-app.git
cd kanban-board-app
```

2. Install dependencies
```bash
npm install
```

3. Start the development server
```bash
npm start
```

The application will open in your default browser at `http://localhost:3000`

## Technologies Used
- React
- TypeScript
- Redux Toolkit
- React Beautiful DnD
- Material-UI
- UUID for unique task IDs

## Project Structure
```
src/
├── components/
│   ├── KanbanBoard.tsx
│   ├── KanbanColumn.tsx
│   └── TaskCard.tsx
├── redux/
│   ├── store.ts
│   └── taskSlice.ts
├── types/
│   └── task.ts
└── App.tsx
```

## Usage
- Drag and drop tasks between columns
- Use the search bar to filter tasks
- Click "Add Task" to create a new task in the To Do column

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.
