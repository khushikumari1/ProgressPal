# ProgressPal - Smart Lecture Video Progress Tracker

**ProgressPal** is a smart, intuitive, and highly efficient video progress tracking system designed to help students track their progress while watching lecture videos. The system ensures that only genuine watched intervals are counted, skipping doesn't cheat the system, and progress can be saved and resumed accurately. It provides a seamless user experience, allowing students to freely seek through the video while ensuring that only the new watched time is recorded.

## Features

- Smart Progress Tracking: Tracks genuine watched intervals and prevents cheating by skipping.
- Save and Resume Progress: Users can save their progress and resume watching from where they left off.
- Flexible Video Controls: Users can freely seek through the video without losing progress.
- Custom Progress Bar: The UI visually renders watched segments, providing a smooth and intuitive experience.
- No Restrictions on Controls: The system doesn't limit the user’s interaction with the video, prioritizing an excellent user experience.

## Technologies Used

- Backend: FastAPI
- Frontend: ReactJS
- Database: SQLAlchemy
- YouTube Integration: react-youtube

## Setup Instructions

### Prerequisites

- Python 3.x
- Node.js and npm
- PostgreSQL (or any SQL database)

### Backend Setup

1. Clone the repository:
   git clone https://github.com/khushikumari1/progresspal.git
   cd progresspal

2. Set up a virtual environment:
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Set up the database and apply migrations:
   alembic upgrade head

5. Create a `.env` file:
   DATABASE_URL=postgresql://username:password@localhost/dbname  
   JWT_SECRET=your_secret_key

6. Start the backend server:
   uvicorn main:app --reload

### Frontend Setup

1. Navigate to the frontend:
   cd video-tracker-front

2. Install dependencies:
   npm install

3. Start the development server:
   npm start

### Running the Project

- Backend: http://localhost:8000
- Frontend: http://localhost:3000

## API Endpoints

- GET /progress/{user_id}/{video_id}
- POST /progress/{user_id}/{video_id}

Example POST Body:
{
  "watched_intervals": [
    {"start": 0, "end": 30},
    {"start": 60, "end": 90}
  ]
}

## Planned Features

- Video Selector
- Hover Tooltips on Progress Bar
- Heatmap Visualization
- Circular Progress Component
- Responsive UI + Dark Mode

## Contributing

1. Fork the repository.
2. Create a new branch.
3. Commit your changes.
4. Push and open a pull request.

## License

MIT License

