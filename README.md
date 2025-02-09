 _____  _                   _____ _                           
|  __ \(_)                 / ____| |                          
| |  | |_ _ __  _   _    | (___ | |__   __ _ _ __ _ __ ___   __ _ 
| |  | | | '_ \| | | |    \___ \| '_ \ / _` | '__| '_ ` _ \ / _` |
| |__| | | |_) | |_| |    ____) | | | | (_| | |  | | | | | | (_| |
|_____/|_| .__/ \__,_|   |_____/|_| |_|\__,_|_|  |_| |_| |_|\__,_|
         | |                                                   
         |_|                                                   

                    Developer: Dipu Sharma

# Event Management System

A robust event management system built with Python, featuring APIs for event creation, attendee management, and asynchronous task processing.

## Features

- Event creation and management
- Attendee registration and tracking
- Asynchronous task processing with Celery
- RESTful API endpoints
- Scalable architecture

## Tech Stack

- Python
- FastAPI/Flask (Web Framework)
- Celery (Task Queue)
- Database (Postgresql)
- RESTful APIs

## Project Structure

```
Event_Management/
├── src/
│   ├── api/
│   │   ├── event/
│   │   │   └── router.py
|   |   |   └── tasks.py
│   │   └── attendee/
│   │       ├── router.py
│   │       └── tasks.py
│   └── worker/
│       └── celery_worker.py
├── .gitignore
└── README.md

```

## Setup and Installation

1. Clone the repository

```bash
git clone <repository-url>
cd Event_Management
```

2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Configure environment variables

```bash
cp .env.text .env
# Edit .env with your configuration
```

5. Start the application

```bash
# Start the web server
python main.py

# Start Celery worker (in a separate terminal)
celery -A src.worker.celery_worker worker --loglevel=info
```

# Start Celery Beat(in a separate terminal)

celery -A src.worker.celery_worker beat --loglevel=info

## API Documentation

- `/api/events/`: Event management endpoints
- `/api/attendees/`: Attendee management endpoints

For detailed API documentation, visit `/docs` or `/redoc` when the server is running.
