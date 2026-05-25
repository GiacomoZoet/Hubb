# Hubb

A real-time team messaging web app built as a final year university project. Think Slack but simpler, self-hostable, and completely free — workspaces, channels, direct messages, and live updates over WebSocket.

## What it does

- Create and join workspaces (called "hubbs")
- Public and private channels within each workspace, with real-time messaging
- Direct messages between users, also real-time
- Invite members to workspaces and private channels by username
- Link previews with Open Graph metadata for URLs in messages
- Email confirmation on registration
- Password reset by email
- JWT authentication with silent token refresh — no unexpected logouts
- Rate limiting (5 messages per 5 seconds per user)
- Dark mode
- Fully mobile-optimised layout with a bottom tab navigation

## Tech stack

**Backend** — Flask, Flask-SocketIO, Flask-JWT-Extended, SQLAlchemy, PostgreSQL  
**Frontend** — Vue 3, Vite, Pinia, Vue Router, Tailwind CSS, socket.io-client

## Project structure

```
backend/
  src/
    app/
      models/       # SQLAlchemy models
      routes/       # REST API blueprints
      sockets/      # Socket.IO event handlers
      utils/        # Decorators, email helpers
    tables.sql      # PostgreSQL schema
    run.py
frontend/
  src/
    api/            # Axios API calls
    components/     # Vue components
    stores/         # Pinia stores
    views/          # Page-level components
    router/
```

## Running locally

You need Python 3.11+, Node 20+, and a PostgreSQL database.

**Database**

Create a database and run the schema:

```bash
psql -U your_user -d your_db -f backend/src/tables.sql
```

**Backend**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in `backend/src/`:

```
SECRET_KEY=your-secret
JWT_SECRET_KEY=your-jwt-secret
DB_HOST=localhost
DB_PORT=5432
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_db
RESEND_API_KEY=your-resend-api-key
FRONTEND_URL=http://localhost:5173
```

Then run:

```bash
.venv/bin/python src/run.py
```

Backend runs on port 5001.

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on port 5173. API calls are proxied to the backend via Vite.

## API

The REST API is mounted at `/api`. Main endpoints:

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/auth/register | Register |
| POST | /api/auth/login | Login |
| POST | /api/auth/refresh | Refresh access token |
| POST | /api/auth/logout | Logout |
| POST | /api/auth/forgot-password | Request password reset |
| POST | /api/auth/reset-password | Set new password |
| GET | /api/workspaces/ | List workspaces |
| POST | /api/workspaces/ | Create workspace |
| POST | /api/workspaces/:id/invite | Invite member by username |
| GET | /api/channels/:workspace_id/channels | List channels |
| POST | /api/channels/:workspace_id/channels | Create channel |
| GET | /api/messages/:channel_id | Get messages |
| POST | /api/messages/:channel_id | Send message |
| GET | /api/messages/search?q=term | Full-text message search |
| GET | /api/dm/:user_id | Get direct message history |
| POST | /api/dm/:user_id | Send direct message |
| GET | /api/og?url=... | Open Graph proxy for link previews |

Real-time events are handled over WebSocket using Socket.IO.

## Notes

- Access tokens last 15 minutes; refresh tokens last 30 days and are stored in the database so they can be revoked
- Socket.IO connection is established on workspace load; users join a personal room (`user_<id>`) for DM and invitation notifications
- Private channels are filtered at the SQL query level — non-members cannot see them even via the API
- All database queries go through SQLAlchemy ORM; the one raw SQL query (full-text search) uses bound parameters — no SQL injection surface
- Workspace deletion cascades to all channels, messages, and members at the database level
- In production the backend is deployed on Render and kept alive via a `/healthz` ping from UptimeRobot
