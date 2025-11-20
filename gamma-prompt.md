## Prompt for Gamma AI

Create a slide deck titled **“Coffee Corner – Final Project Stage 3 Presentation & Demo.”**  
Audience: software engineering instructors evaluating Stage 3 (presentation & demo).  
Tone: confident, reflective, technically clear. Use Coffee Compass brand colors (espresso brown, latte beige, accent orange) and minimal line illustrations of cups/compass icons. Aim for 8–10 slides geared for a 4–6 minute talk.

The deck must cover, in order:

1. **Title & Purpose** – project name, team members, and a one-sentence purpose emphasizing ideas/reasoning/design insight.
2. **Project Overview** – goal, target users, top features; mention quick entry recommendations, places search, journal/saved flows.
3. **System Design & Architecture** – describe major modules (accounts, shops, reviews, journal, recommendations), main data flows, and how Django REST + Postgres supports them; include bullet callouts for core classes/models and a simplified diagram placeholder.
4. **Engineering Reasoning & Design Choices** – explain why certain relationships, APIs, or UI funnels were adopted; highlight trade-offs (e.g., template-driven views vs. SPA, Postgres for relational integrity).
5. **Design Patterns & OOP Principles** – list any applied/planned patterns (Serializer abstractions, DRF view decorators, repository-like service layers) and how encapsulation + inheritance were used.
6. **Testing, Debugging & Iteration** – cover migration strategy, `manage.py check`, API smoke tests, and any manual/automated verification loops; note partial coverage and next planned test cases.
7. **Challenges & Lessons Learned** – bullets about handling template loading, host configs, nav scaffolding, integrating auth requirements, and balancing UX polish with backend reliability.
8. **Reflection & Future Work** – what surprised us, how we would improve (e.g., add richer data viz, expand recommendation engine, tighten auth for posting), and personal growth as designers/collaborators/problem solvers.
9. **Call to Action / Demo Plan** – specify what will be shown live (nav walkthrough, API responses) and invite questions.

Each slide should:
- Use concise bullet points (no paragraphs) plus optional iconography.
- Highlight rubric keywords: understanding of design & architecture, engineering reasoning, design patterns, process reflection, communication, team participation.
- Reserve space for speaker notes summarizing the key talking point per slide.

Do not fabricate data beyond what’s implied; if something is incomplete, phrase it as “in progress” with next steps. Ensure the narrative focuses on **how we think and design**, not just the finished product.***

---

### Collaboration Plan (for slide notes & speaker narration)
- **Division of work:** Teammate A (friend) owns the first four nav pages (Home, Places, Products, Saved). Teammate B (me) owns the remaining four (Blog, Help, Contact, Auth flows). Each person builds their templates/components while reusing the shared `base.html` shell so navigation persists.
- **Workflow:** Use separate Git branches (e.g., `feature/nav-first-half`, `feature/nav-second-half`). Commit page-level changes independently, then merge into `main` via pull requests.
- **Combining changes:** Before final merge, both developers pull latest `main`, resolve any template conflicts (mostly in shared `base.html` or CSS), and run `python manage.py check` plus a manual click-through to confirm all eight routes render with the nav intact. Finish with a final PR summarizing the combined UI work so the presentation/demo can show the unified experience.
