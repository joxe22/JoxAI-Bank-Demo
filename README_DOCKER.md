### Dockerized setup

- Build and run:
```bash
docker compose --env-file .env up --build
```

- Environment file:
  - Copy `.env.example` to `.env` and adjust values.

- Services:
  - app: FastAPI + Gunicorn at http://localhost:8000 (WebSockets supported)
  - db: Postgres 15 with persistent volume `db-data`

- Health endpoints:
  - `GET /health` (liveness)
  - `GET /readiness` (readiness + DB)

- Apply DB migrations: automatically on startup (configurable with `AUTO_MIGRATE=true`).

- Frontend:
  - The React admin panel is built in the image and served by FastAPI from `banking_chatbot/frontend/admin-panel/dist`.
  - For local dev of the admin panel, run Vite on host and point `VITE_API_URL`/`VITE_WS_URL` envs to the backend.

- Common commands:
```bash
# Rebuild after code changes
docker compose build app && docker compose up app

# Tail logs
docker compose logs -f app

# Run Alembic migrations manually
docker compose exec app alembic -c /app/banking_chatbot/backend/alembic.ini upgrade head

# Open interactive shell
docker compose exec app bash
```
