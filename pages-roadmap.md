## Coffee Compass Pages Roadmap

Your focus is building the HTML templates that live under `templates/` (plus any component partials you want to keep inside each app). The Django views/API endpoints already exist, so most of your work is wiring up UI, calling the APIs from JavaScript when needed, and making sure the experience feels cohesive.

### Environment setup
1. Install deps: `pip install -r requirements.txt`
2. Start services: `docker compose up` (or run Django locally with Postgres if you prefer)
3. The dev server runs on `http://localhost:8000` and watches files inside `templates/`

### Global layout tasks
- Introduce a `templates/base.html` with the site shell (header, nav, footer); land the existing `home.html` inside `{% block content %}` and extend from there on other pages.
- Add a shared stylesheet in `static/` (or inline Tailwind/utility classes if you prefer) to keep typography, spacing, and colors consistent with the landing page palette.
- Drop in a `templates/partials/navbar.html` if it helps keep things DRY.

### Page-level work
| Page | URL | Data source | What to build |
| --- | --- | --- | --- |
| Landing | `/` | Static | Polish the hero, add CTA + a short "How it works" section with icon cards. |
| Shops list | `/shops/` (create template + simple view) | `GET /api/shops/` | Grid/list of coffee shops, filters (search, tags), card showing rating, price, tags. |
| Shop detail | `/shops/<id>/` | `GET /api/shops/<id>` + `/api/shops/<id>/menu` | Hero banner with name/address/map placeholder, hours, tags, then menu sections. |
| Reviews feed | `/reviews/` | `GET /api/reviews?shopId=` | Timeline of latest reviews, filter by shop, include “add review” drawer (POST `/api/reviews/create`). |
| Favorites | `/favorites/` (gated) | `GET /api/reviews/favorites` | Showcase the user’s saved shops with quick links to detail pages plus “remove” buttons. |
| Journal | `/journal/` | `GET /api/journal/entries` (see app) | List-style view showing tasting notes, bean info, brew method badges. |
| About | `/about/` | Static | Story, mission, team photos. |

### Implementation notes
- Use Django template tags for routing: `{% url "home" %}`, etc. and add new entries to `coffee_compass/urls.py` plus per-app `urls.py`.
- For API calls, sprinkle a little vanilla JS `fetch` in `<script>` tags or pull in Alpine.js/HTMX if it will speed you up.
- When posting data, leverage Django’s CSRF token: `{% csrf_token %}` + include the token in AJAX headers.
- Keep accessibility in mind (semantic headings, `aria-label`s, keyboard-friendly controls).
- Update `static/` with any shared images/icons. Remember to reference them with `{% static "path/to/file" %}` after adding `django.contrib.staticfiles`.

Ping me once you scaffold the base template and shops list—we can iterate on data bindings together afterward. Have fun! 🎉
