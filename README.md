CoffeeCorner
CoffeeCorner is a full-stack Django web application that helps users discover, review, and track their favorite coffee shops.
It combines user accounts, shop search, reviews, and a personal coffee journal with basic sentiment-aware recommendations.

Team:
Kerri Jensen (kerrijensen13@gmail.com)
Jeshua Herrera (jeshuah04@gmail.com)

1. Project Overview
CoffeeCorner lets users:

Create an account and sign in
Browse and view coffee shops
Save favorites and see shop details
Write reviews for shops
Keep a private journal about their coffee experiences
Receive simple recommendations and quotes based on user moods
Explore static marketing pages (home, help, contact, etc.)
The backend is built with Django and PostgreSQL, with a small machine learning component using scikit-learn for text sentiment / feature extraction.

2. Tech Stack
Language: Python 3.13
Web Framework: Django
Database: PostgreSQL (via Docker) or SQLite (local dev, if configured)
ML / NLP: scikit-learn (TfidfVectorizer)
Containerization: Docker + Docker Compose
Front-end: Django templates (HTML/CSS), static images/assets
3. Repository Structure
This project follows a standard Django application layout. Instead of placing everything under /src/, Django organizes functionality by "apps," each responsible for a specific feature domain (accounts, shops, reviews, journal, etc.).

Below is the structure of this repository:

COFFESHOP/
├── accounts/                 # User authentication and account management
├── api/                      # (Optional) API routing or shared API helpers
├── coffee_compass/           # Django project settings, URLs, WSGI/ASGI setup
│   ├── settings/             # Base/dev/prod environment configurations
│   └── urls.py               # Root URL dispatcher
├── common/                   # Shared utilities and helper modules
├── journal/                  # Personal journal entries and related logic
├── ops/                      # Operational scripts / deployment utilities
├── recommendations/          # Recommendation engine + ML sentiment analysis
├── reviews/                  # Shop reviews and user ratings
├── shops/                    # Coffee shop models, views, serializers, seeds
├── static/                   # Static assets (logos, images, CSS)
├── templates/                # HTML templates (base layout + pages)
│
├── venv/                     # Local virtual environment (ignored in Git)
│
├── .env                      # Local environment variables (not committed)
├── .env.example              # Template environment file
├── .gitignore                # Files and folders ignored by Git
├── docker-compose.yml        # Docker orchestration for app + database
├── Dockerfile                # Build instructions for Django container
├── entrypoint.sh             # Startup script for Docker service
├── Makefile                  # Optional helper commands for development
├── manage.py                 # Standard Django management script
├── main.py                   # Unified entry point required by assignment
├── pyproject.toml            # Project metadata / tool configuration
├── README.md                 # Project overview and documentation
└── requirements.txt          # Python dependencies