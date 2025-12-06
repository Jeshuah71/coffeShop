DESIGN – Coffee Corner (coffee_compass)

1) Overview
- Django 5 app with server-rendered pages plus JSON APIs for accounts, shops, reviews/favorites, journals, and lightweight recommendations (shop ranker + TF-IDF “Catbot” + toy sentiment-based quotes).
- Default SQLite for quick dev; PostgreSQL when `POSTGRES_HOST` is set (Docker Compose uses Postgres 16). CORS is open for development.
- Optional Google Maps API key injected into templates for map widgets.

2) Architecture
- Apps: `accounts`, `shops`, `reviews`, `journal`, `recommendations`, plus `coffee_compass` (project settings/URLs) and stubs (`api`, `common` not wired into URLs).
- Routing: `coffee_compass/urls.py` serves public pages and mounts app APIs under `/api/*`.
- Views: DRF function-based views for JSON; Django template views for marketing pages and Catbot page.
- Settings: `coffee_compass/settings.py` switches SQLite/Postgres based on env vars; loads `.env` if present; Django sessions for auth.
- Static/UI: `templates/` and `static/` provide the front-end layout.

3) Runtime & Configuration
- Env vars (examples): `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `ALLOWED_HOSTS`, `POSTGRES_HOST/DB/USER/PASSWORD/PORT`, `GOOGLE_MAPS_API_KEY`.
- Local (SQLite): `pip install -r requirements.txt`, `python manage.py migrate`, `python manage.py runserver 0.0.0.0:8000`.
- Docker Compose (Postgres 16): `docker compose up --build` after `.env` is set (with `POSTGRES_HOST=db`). `entrypoint.sh` waits for DB then migrates.

4) Data Model (simplified)
- User (Django auth)
  - Profile (OneToOne) tracks favorite_count, journal_count.
  - Reviews (1..N) with rating/comment; Favorites (many shops).
  - JournalEntries (1..N) with shop, optional menu item, visit date, rating, notes.
- CoffeeShop with avg_rating, rating_count, tags, lat/lon, menu items.
- MenuItem belongs to CoffeeShop.
- Quote with mood_tag (used by recommendations sentiment flow).

5) Core Behaviors
- Accounts: signup/login/logout via session auth; `/api/auth/me` and `/api/auth/profile` return user/profile data.
- Shops: list with query/tag filters and optional haversine distance when lat/lon provided; detail and menu endpoints.
- Reviews/Favorites: create review updates rolling average on the shop; add/remove/list favorites.
- Journal: list/create entries; creation increments profile counters and notifies observers for cached quotes/recommendations.
- Recommendations: text-to-tag shop ranking (`/api/recommendations/`) and TF-IDF Catbot (`/api/recommendations/catbot`); sentiment model (scikit-learn) picks a mood-tagged quote when available.
- Frontend pages: home, places, products, saved, journal, blog, help, contact, get-started, catbot (Catbot UI backed by the API).

6) Request Flow
Client → `coffee_compass/urls.py` → app `urls.py` (API) or template view → view logic/service helpers → database → JSON or HTML response.

7) Key Design Decisions
- Feature-per-app structure to keep domains isolated (accounts, shops, reviews, journal, recommendations).
- Simple services for recommendations, distance (haversine), and sentiment to keep views thin and swappable.
- Session authentication to align with server-rendered pages; CORS left open for development use.
- Environment-driven DB selection to allow SQLite (quick dev) or Postgres (Compose/production-like).

8) Future Improvements
- Harden auth (password reset, email verification, CSRF/CORS tightening for production).
- Expand recommendation logic beyond heuristic tags (collaborative filtering or embeddings).
- Add automated tests and CI runs.
- Improve UI responsiveness and add validation/feedback on forms.
