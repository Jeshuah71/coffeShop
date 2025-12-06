README - Coffee Corner (coffee_compass)

Django 5 app for discovering, reviewing, and journaling coffee shops. Serves server-rendered pages for accounts, shops, reviews, journals, and lightweight recommendations (including a TF-IDF “Catbot”).

Features
- Public pages: home, places, products, saved, journal, blog, help, contact, get-started, catbot (maps use Google Maps API key).
- Session auth: signup, login/logout; `Profile` tracks journal and favorite counts.
- Shops: filter by tags with optional distance hints (haversine on stored lat/lon), detail, and menu endpoints.
- Reviews/Favorites: create reviews (updates rolling average rating), list reviews, add/remove favorites.
- Journal: create entries (shop + optional menu item, visit date, rating, notes); creation bumps profile counters and triggers cached quote/recommendation observers.
- Recommendations: text-to-tag shop ranking and a TF-IDF chatbot; toy scikit-learn sentiment model selects mood-tagged quotes.

Stack
- Python 3.13, Django 5, Django REST Framework, django-cors-headers.
- DB: SQLite by default; PostgreSQL when `POSTGRES_HOST` is set (Compose uses Postgres 16).
- ML: scikit-learn (TfidfVectorizer + LogisticRegression) for sentiment/chat similarity.
- Front end: Django templates + static assets; optional Google Maps API key for templates.

Project Layout
- `coffee_compass/` – settings, URLs, simple page renders.
- `accounts/`, `shops/`, `reviews/`, `journal/`, `recommendations/` – core apps/APIs.
- `templates/`, `static/` – UI templates and assets.
- `docker-compose.yml`, `Dockerfile`, `entrypoint.sh`, `requirements.txt`, `manage.py` – runtime tooling.
- `api/`, `common/` – stubs not wired into the main URL config.

Configuration
Export env vars or place them in `.env`:
```
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,web
POSTGRES_HOST=             # leave empty to use SQLite
POSTGRES_DB=coffee_compass
POSTGRES_USER=cc_user
POSTGRES_PASSWORD=supersecret
POSTGRES_PORT=5432
GOOGLE_MAPS_API_KEY=     
```

Local Development (SQLite)
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Docker Compose (Postgres)
1) Add a `.env` with the vars above (set `POSTGRES_HOST=db`; set `DJANGO_DEBUG=False` if desired).
2) Start:
```
docker compose up --build
```
`entrypoint.sh` waits for Postgres, runs migrations, and serves on http://localhost:8000.

API Outline
- Accounts: `POST /api/auth/signup`, `POST /api/auth/login`, `POST /api/auth/logout`, `GET /api/auth/me`, `GET /api/auth/profile`.
- Shops: `GET /api/shops?query=&tags=&lat=&lon=`, `GET /api/shops/<id>`, `GET /api/shops/<id>/menu`.
- Reviews/Favorites: `GET /api/reviews?shopId=`, `POST /api/reviews/create` (auth), `GET /api/reviews/favorites` (auth), `POST /api/reviews/favorites/add` (auth), `DELETE /api/reviews/favorites/<shop_id>` (auth).
- Journal: `GET /api/journal/` (auth), `POST /api/journal/create` (auth).
- Recommendations: `POST /api/recommendations/` (text prompt), `POST /api/recommendations/catbot` (chatbot).

Notes
- Auth uses Django sessions; CORS is open for development.
- Without `POSTGRES_HOST`, SQLite is used at `db.sqlite3` in the project root.
