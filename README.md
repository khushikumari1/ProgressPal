# ProgressPal - Smart Lecture Video Progress Tracker

**ProgressPal** is a smart, intuitive, and highly efficient video progress tracking system designed to revolutionize the way students engage with educational video content. It goes beyond traditional video completion logic by ensuring that only genuinely watched content is counted — even if the student skips or rewatches, their progress is tracked accurately. Built with performance, scalability, and user experience in mind, ProgressPal delivers precision, persistence, and interactivity all in one.

---

## ✨ Features

- 🎯 **Smart Progress Tracking:** Accurately tracks only the newly watched intervals to prevent cheating via skipping or rewatching.
- 💾 **Save & Resume:** User progress is persistently stored and automatically resumed across sessions.
- 🎥 **Seamless Video Controls:** Users are free to seek, pause, replay, or skip — the system still only logs meaningful progress.
- 📊 **Dynamic Custom Progress Bar:** Visually renders watched segments with intuitive feedback.
- 🚀 **User-Centric Experience:** Empowers students with freedom while maintaining precision in learning analytics.

---

## 🧰 Technologies Used

- ⚙️ **Backend:** FastAPI (Python)
- 🖥️ **Frontend:** ReactJS
- 🗃️ **Database:** PostgreSQL with SQLAlchemy ORM
- 📺 **Video Integration:** YouTube Player via `react-youtube`

---

## ⚙️ Setup Instructions

### 🔧 Prerequisites

- Python 3.x
- Node.js and npm
- PostgreSQL (or compatible SQL database)

### 🛠️ Backend Setup

```bash
git clone https://github.com/khushikumari1/progresspal.git
cd progresspal
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:
```env
DATABASE_URL=postgresql://username:password@localhost/dbname
JWT_SECRET=your_secret_key
```

Apply database migrations:
```bash
alembic upgrade head
```

Start the server:
```bash
uvicorn main:app --reload
```

### 🌐 Frontend Setup

```bash
cd video-tracker-front
npm install
npm start
```

Access the app at:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

---

## 📡 API Endpoints

- `GET /progress/{user_id}/{video_id}` – Fetch saved progress
- `POST /progress/{user_id}/{video_id}` – Submit updated watched intervals

**Example POST Body:**
```json
{
  "watched_intervals": [
    {"start": 0, "end": 30},
    {"start": 60, "end": 90}
  ]
}
```

---

## 📐 Design Documentation

### 🔍 Tracking Watched Intervals

ProgressPal captures user activity per second, tracking when a video is playing and logging start-end intervals in real time. The frontend stores these intervals and pushes them to the backend upon pause, end, or regular intervals.

```json
[
  { "start": 10, "end": 30 },
  { "start": 60, "end": 90 }
]
```

### 🔗 Merging Intervals to Avoid Duplication

To ensure that rewatched or overlapping intervals don't bloat the progress, the backend merges new intervals with those already stored:

#### Before:
```json
Old: [{ "start": 0, "end": 20 }, { "start": 50, "end": 70 }]
New: [{ "start": 10, "end": 30 }, { "start": 60, "end": 80 }]
```
#### After Merging:
```json
Merged: [{ "start": 0, "end": 30 }, { "start": 50, "end": 80 }]
```

The merging logic ensures that progress is based solely on **unique seconds watched**.

### 📊 Calculating Progress Percentage

```text
Unique Seconds Watched = Σ (merged intervals)
Video Duration = Total video length
Progress (%) = (Unique Seconds Watched / Video Duration) × 100
```

The frontend periodically recalculates this value and updates the visual progress bar.

### 💾 Persistent Save & Seamless Resume

- Each user's progress is stored with their `user_id` and `video_id`.
- When a user returns, the video resumes exactly from the last saved timestamp.
- Watched segments are visually rendered, and total progress is instantly visible.

### 🧠 Design Decisions & Challenges

| Challenge | Solution |
|----------|----------|
| Avoiding inflated progress from rewatching | Custom interval merging avoids duplicate counting |
| Preventing cheating via skipping | Skipped segments aren’t recorded unless watched fully |
| Buffering/seeking glitches | Tracked with debounce timers to minimize noisy events |
| Stateful session management | Implemented JWT-based endpoints for secure persistence |

---

## 🚀 Planned Enhancements

- 🎞️ Video Selector Dropdown
- 🖱️ Hover Tooltips on Watched Segments
- 🌡️ Heatmap Visualization of Attention
- 🔵 Circular Progress Dial for Completion
- 🌙 Responsive UI with Dark Mode

---

## 🤝 Contributing

We welcome contributions from the community:
1. Fork the repository
2. Create a new feature branch
3. Make your changes
4. Commit and push with meaningful messages
5. Open a pull request with a detailed description

---

## 📄 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it as needed!

