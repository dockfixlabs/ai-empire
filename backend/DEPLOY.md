# AI Empire Cloud Deployment Guide

## Option 1: Railway (Recommended — easiest)

1. Install Railway CLI: `iwr https://railway.app/install.ps1 | iex`
2. Login: `railway login`
3. Init: `railway init`
4. Set environment variables:
   ```
    railway env set GROQ_API_KEY=<your-groq-api-key>
   railway env set SECRET_KEY=<generate-a-random-secret>
   railway env set DATABASE_URL=postgresql+asyncpg://...
   railway env set GUMROAD_API_KEY=<your-gumroad-token>
   ```
5. Deploy: `railway up`
6. Add a PostgreSQL plugin from Railway dashboard
7. Set `DATABASE_URL` to Railway's PostgreSQL connection string (use `+asyncpg` variant)
8. For frontend: add a separate Railway service from `frontend/` directory

## Option 2: DigitalOcean App Platform

1. Push code to GitHub
2. Go to cloud.digitalocean.com → Apps → Create App
3. Connect your GitHub repo
4. Set up backend service:
   - Run command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - HTTP port: 8000
   - Add env vars (same as Railway above)
5. Set up frontend static site:
   - Build command: `cd frontend && npm install && npm run build`
   - Output dir: `frontend/dist`
   - Add env var: `VITE_API_URL=https://your-backend.ondigitalocean.app`
6. Add managed PostgreSQL database
7. Deploy

## Option 3: PythonAnywhere

1. Create account on pythonanywhere.com (paid plan for web apps)
2. Open Bash console
3. Clone repo: `git clone https://github.com/yourusername/gumroad-ai-empire.git`
4. Set up virtualenv: `mkvirtualenv empire --python=python3.11`
5. Install deps: `pip install -r backend/requirements.txt`
6. Set up web app via Web tab:
   - Manual config → Python 3.11
   - WSGI file pointing to `app.main:app`
   - Set env vars in WSGI file
7. For frontend: build locally and upload to static files
8. Set up scheduled task (Tasks tab) to keep the agent scheduler alive

## Option 4: VPS (DigitalOcean Droplet / Linode)

1. Create Ubuntu 22.04 VPS
2. SSH in and run:
   ```bash
   # Install deps
   curl -fsSL https://deb.nodesource.com/setup_20.x | sudo bash -
   sudo apt-get install -y nodejs python3.11 python3.11-venv git nginx

   # Clone repo
   git clone https://github.com/yourusername/gumroad-ai-empire.git
   cd gumroad-ai-empire

   # Backend setup
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r backend/requirements.txt

   # Frontend setup
   cd frontend
   npm install
   npm run build
   cd ..

   # Create systemd service
   sudo tee /etc/systemd/system/empire-backend.service << 'EOF'
   [Unit]
   Description=AI Empire Backend
   After=network.target

   [Service]
   User=root
   WorkingDirectory=/root/gumroad-ai-empire/backend
   Environment="GROQ_API_KEY=gsk_..."
   Environment="SECRET_KEY=..."
   Environment="DATABASE_URL=sqlite+aiosqlite:///./gumroad_ai.db"
   ExecStart=/root/gumroad-ai-empire/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   EOF

   sudo systemctl enable empire-backend
   sudo systemctl start empire-backend

   # Configure nginx
   sudo tee /etc/nginx/sites-available/empire << 'EOF'
   server {
       listen 80;
       server_name your-domain.com;

       root /root/gumroad-ai-empire/frontend/dist;
       index index.html;

       location /api {
           proxy_pass http://localhost:8000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
       }

       location / {
           try_files $uri $uri/ /index.html;
       }
   }
   EOF

   sudo ln -s /etc/nginx/sites-available/empire /etc/nginx/sites-enabled/
   sudo nginx -t && sudo systemctl reload nginx
   ```

## Environment Variables (all options)

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | Yes | Groq API key for AI |
| `SECRET_KEY` | Yes | Random string for JWT signing |
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `GUMROAD_API_KEY` | Yes | Gumroad Personal Access Token |
| `OPENAI_API_KEY` | No | OpenAI fallback |
| `MAILGUN_API_KEY` | No | Email sending |
| `MAILGUN_DOMAIN` | No | Email domain |

## Keeping the Scheduler Alive

The scheduler runs as an asyncio background task inside the FastAPI process. To ensure 24/7 operation:

- **Railway**: Built-in keep-alive. Set `CRON` or use Railway's cron jobs.
- **DigitalOcean**: App Platform keeps the process running automatically.
- **VPS**: systemd `Restart=always` ensures it restarts on crash.
- **PythonAnywhere**: Use "Always-on" task or set up a cron job to hit the health endpoint every 5 minutes.

## Database Migration (SQLite → PostgreSQL)

1. Install `pgloader` or use Alembic
2. Dump SQLite: `sqlite3 gumroad_ai.db .dump > dump.sql`
3. Import to PostgreSQL: `psql $DATABASE_URL < dump.sql`
4. Update `DATABASE_URL` in env vars to point to PostgreSQL
5. Ensure the URL uses `+asyncpg` for async SQLAlchemy:
   `postgresql+asyncpg://user:pass@host:5432/dbname`

## Monitoring

- Health endpoint: `GET /health` returns `{"status": "healthy"}`
- The scheduler logs to stdout — check `railway logs` or `journalctl -u empire-backend`
- WebSocket endpoint `ws://your-domain.com/api/v1/agents/ws` streams all agent activity
