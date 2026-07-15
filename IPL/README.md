# IPL Predictor - Full-Stack Application Setup Guide

## Project Overview

IPL Predictor is a comprehensive machine learning application for predicting Indian Premier League (IPL) match outcomes, scores, player performance, and viewership metrics.

### Directory Structure

```
IPL/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models (SQLAlchemy)
│   │   ├── routes/          # API endpoints
│   │   ├── schemas/         # Pydantic validation schemas
│   │   ├── database/        # Database utilities
│   │   ├── config.py        # Settings & environment config
│   │   ├── logger.py        # Logging setup
│   │   └── main.py          # FastAPI application
│   ├── data/                # Raw and processed datasets
│   ├── notebooks/           # Jupyter notebooks for EDA
│   ├── mlflow_artifacts/    # MLflow models & tracking
│   ├── models/              # Trained ML models
│   ├── tests/               # Unit and integration tests
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Backend container configuration
│   ├── docker-compose.yml   # Multi-container orchestration
│   └── .env.example         # Environment variables template
│
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable React components
│   │   ├── pages/           # Page components (Dashboard, Predictor, etc.)
│   │   ├── services/        # API client utilities
│   │   ├── store/           # Zustand state management
│   │   ├── App.js           # Main application component
│   │   └── index.js         # Entry point
│   ├── public/              # Static assets
│   ├── package.json         # Dependencies and scripts
│   ├── tailwind.config.js   # Tailwind CSS configuration
│   ├── Dockerfile           # Frontend container
│   └── .env.example         # Frontend environment variables
│
└── android/
    └── (Kotlin project structure - coming in Step 7)
```

## Installation & Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+ (or Docker)
- Docker & Docker Compose (optional, for containerized setup)

### Step 1: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your actual values:
# - DATABASE_URL: postgresql://user:password@localhost:5432/ipl_predictor
# - REDIS_URL: redis://localhost:6379/0
# - SECRET_KEY: Generate a secure random key
# - KAGGLE_USERNAME and KAGGLE_KEY for data download
```

### Step 2: Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Edit .env:
# REACT_APP_API_URL=http://localhost:8000/api
```

### Step 3: Database & Cache Setup

#### Option A: Using Docker Compose (Recommended)

```bash
# From root directory
docker-compose up -d

# Verify services
docker-compose ps
```

#### Option B: Manual Setup

**PostgreSQL:**
```bash
# Create database
createdb -U postgres ipl_predictor

# Run migrations (when ready)
alembic upgrade head
```

**Redis:**
```bash
# Using Docker
docker run -d -p 6379:6379 redis:7-alpine

# Or install locally and run
redis-server
```

### Step 4: Running the Application

**Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app/main.py
```

API will be available at: http://localhost:8000
API Docs: http://localhost:8000/docs

**Frontend:**
```bash
cd frontend
npm start
```

Application will be available at: http://localhost:3000

## API Endpoints

### Health Check
- `GET /health` - Server health status
- `GET /api/version` - API version

### Predictions (Coming in Step 3)
- `POST /api/predictions/match-winner` - Predict match winner
- `POST /api/predictions/score` - Predict match score
- `POST /api/predictions/player-stats` - Predict player statistics
- `POST /api/predictions/viewership` - Estimate viewership

### Matches (Coming in Step 2)
- `GET /api/matches` - List all matches
- `GET /api/matches/{id}` - Get match details

### Players (Coming in Step 2)
- `GET /api/players` - List all players
- `GET /api/players/{id}` - Get player details

## Environment Variables

### Backend (.env)
```
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
DATABASE_URL=postgresql://user:password@localhost:5432/ipl_predictor
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
MLFLOW_TRACKING_URI=./mlflow_artifacts
ENVIRONMENT=development
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000/api
```

## Docker Deployment

Build and run all services:

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

Services will be available at:
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## Next Steps

1. **Step 2:** Write data loading and preprocessing scripts
2. **Step 3:** Build ML models with training scripts
3. **Step 4:** Implement FastAPI endpoints
4. **Step 5:** Complete React frontend pages
5. **Step 6:** Finalize Docker setup
6. **Step 7:** Build Android Kotlin application

## Troubleshooting

### Port Already in Use
```bash
# Change port in .env or use:
# On Windows (PowerShell)
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force

# On macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### Database Connection Error
- Ensure PostgreSQL is running
- Verify DATABASE_URL in .env
- Check credentials

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Documentation

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [XGBoost Guide](https://xgboost.readthedocs.io/)
- [TensorFlow/Keras](https://www.tensorflow.org/)

## Support & Contributing

For issues or improvements, please refer to the project documentation and testing guidelines.

---

**Last Updated:** April 2026
**Version:** 1.0.0
