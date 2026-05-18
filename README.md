# Huub

A real-time team messaging web app built as a final year university project. Think Slack but simpler — workspaces, channels, direct messages, and live updates over WebSocket.

## What it does

- Create and join workspaces (called "huubs")
- Channels within each workspace with real-time messaging
- Direct messages between users, also real-time
- Invite members to workspaces by email
- Email confirmation on registration
- Dark mode
- Fully mobile-optimised layout with a bottom tab navigation

## Tech stack

**Backend** — Flask, Flask-SocketIO, Flask-JWT-Extended, SQLAlchemy, MySQL  
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

You need Python 3.11+, Node 20+, and a MySQL database.

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
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your-password
DB_NAME=imessageu
MAIL_USERNAME=your-email
MAIL_PASSWORD=your-app-password
```

Then run:

```bash
cd backend
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
| GET | /api/workspaces/ | List workspaces |
| POST | /api/workspaces/ | Create workspace |
| POST | /api/workspaces/:id/members | Invite member |
| GET | /api/channels/:id/channels | List channels |
| POST | /api/channels/:id/channels | Create channel |
| GET | /api/messages/:id | Get messages |
| POST | /api/dm/:user_id | Send direct message |

Real-time events are handled over WebSocket using Socket.IO.

## Notes

- JWT tokens are stored in localStorage and sent via the Authorization header
- Socket.IO connection is established on workspace load; users join a personal room for DM and invitation notifications
- Workspace deletion cascades to all channels and members at the database level
