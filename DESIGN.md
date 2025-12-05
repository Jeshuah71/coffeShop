DESIGN.md – CoffeeCorner
1. System Overview
CoffeeCorner is a Django-based web application designed to help users discover, review, and track their favorite coffee shops. The system uses Django’s multi-app architecture, where each feature (accounts, shops, reviews, journal, recommendations) is separated into its own app for clarity and maintainability.

The application runs using Docker (Django + PostgreSQL), but can also run locally via python main.py.

2. Architecture
Project Structure
coffee_compass/ – Project configuration (settings, URLs, WSGI/ASGI)
accounts/ – User registration, login, and authentication
shops/ – Coffee shop data, detail pages, and business logic
reviews/ – User reviews and ratings linked to shops
journal/ – Personal user journal entries
recommendations/ – Simple recommendation logic + sentiment analysis (scikit-learn)
templates/ – HTML pages rendered by Django
static/ – Images, CSS, logos
main.py – Assignment-required entry point
How Requests Flow
User request → URL routing → View → Service logic → Database → Template response.

3. Key Design Decisions
(1) Multi-App Django Architecture
We used Django’s recommended structure of splitting features into separate apps.
This makes the code easier to maintain and allows features to evolve independently.

(2) Service Layer for Recommendations
Instead of embedding ML logic in views, we placed sentiment analysis and recommendation logic inside recommendations/services.py.
This separation keeps views simple and allows the ML layer to be improved later.

(3) Docker for Environment Consistency
Docker ensures the project runs the same way for every team member and for the grader (Python version, database, dependencies).

(4) Use of Environment Variables
The system loads sensitive configuration (database credentials, secret keys) from a .env file, following best practices.

4. Data Model (Simplified)
User

has many Reviews
has many JournalEntries
Shop

has many Reviews
stores an aggregate rating
Review

belongs to User + Shop
stores rating + text
JournalEntry

belongs to User
text used by sentiment analyzer
5. Challenges & What We Learned
Merge conflicts
We learned to resolve remote/local changes carefully and ignore __pycache__ files using .gitignore.

Docker rebuilds
Adding ML dependencies (like scikit-learn) required updating requirements.txt and rebuilding the container.

Coordinating URLs and Views
As features expanded, it became more important to keep routing organized using per-app urls.py files.

Overall, we learned not only Django syntax but how to structure a multi-feature application cleanly.

6. Future Improvements
More advanced recommendation system
Better UI/UX and responsive design
API endpoints using Django REST Framework
More thorough automated tests
Shop owner accounts with permissions