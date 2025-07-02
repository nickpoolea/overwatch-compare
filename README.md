# Overwatch Player Comparison Tool

A full-stack application that compares Overwatch player statistics using React frontend and Django backend.

## Features

- Compare two players' statistics for any hero
- Support for quickplay and competitive modes
- Detailed statistics organized by categories (Best, Average, Game, Hero Specific)
- Category summaries showing wins/ties between players
- Responsive design for mobile and desktop

## Project Structure

```
overwatch_compare/
├── backend/               # Django REST API
│   ├── overwatch_api/    # Django project
│   ├── stats/            # Django app
│   └── manage.py
├── frontend/             # React application
│   ├── src/
│   ├── public/
│   └── package.json
├── .venv/                # Python virtual environment
├── start_app.py          # Launch script for both servers
└── start_app.bat         # Windows batch launcher
```

## Setup Instructions

### Prerequisites

- Python 3.11+ installed
- Node.js and npm installed
- Virtual environment activated (`.venv` included)

### Backend Setup (Django)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies (if needed):
   ```bash
   pip install django djangorestframework django-cors-headers requests
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

The backend API will be available at `http://localhost:8000/api/`

### Frontend Setup (React)

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies (if needed):
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

### Easy Launch (Recommended)

For convenience, you can start both servers with a single command:

**Option 1: Python Launcher**
```bash
python start_app.py
```

**Option 2: Windows Batch File**
```bash
start_app.bat
```

**Option 3: VS Code Task**
- Press `Ctrl+Shift+P` → Type "Tasks: Run Task"
- Select "Start Full App" to start both servers simultaneously

## API Endpoints

### GET /api/heroes/
Returns a list of all available heroes.

### POST /api/compare/
Compares two players' statistics for a specific hero.

**Request body:**
```json
{
  "player1": "BaconChee#1321",
  "player2": "Player2#1234", 
  "hero": "ana",
  "gamemode": "quickplay",
  "platform": "pc"
}
```

**Response:**
```json
{
  "hero": "ana",
  "player1": "BaconChee#1321",
  "player2": "Player2#1234",
  "categories": [
    {
      "name": "Best",
      "stats": [...],
      "summary": {
        "player1_wins": 5,
        "player2_wins": 3,
        "ties": 1,
        "player1_average": 123.45,
        "player2_average": 98.76,
        "average_difference": 24.69
      }
    }
  ]
}
```

## Usage

1. Enter two BattleTags in the format `Username#1234`
2. Select a hero from the dropdown
3. Choose gamemode (quickplay/competitive) and platform (pc/console)
4. Click "Compare Players" to see detailed statistics comparison

## Data Source

This application uses the [OverFast API](https://overfast-api.tekrop.fr/) to fetch Overwatch player statistics.

## Technologies Used

- **Frontend**: React, CSS3, HTML5
- **Backend**: Django, Django REST Framework
- **API**: OverFast API
- **HTTP Client**: Fetch API, Python Requests

## Notes

- Player profiles must be public for stats to be accessible
- Statistics are fetched in real-time from the OverFast API
- The application supports all current Overwatch heroes
- CORS is configured to allow requests from localhost:3000
