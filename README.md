# Pastebin & File Host (Terminal Edition)

A fully self-hosted, extremely minimalist, and modern terminal-styled Pastebin and File Hosting server.

## Tech Stack
- **Backend:** Python, Flask, Gunicorn
- **Database:** SQLite, SQLAlchemy
- **Frontend:** HTML, Vanilla CSS, Vanilla JS
- **Infrastructure:** Docker, Docker Compose, GitHub Actions

## Installation & Usage

1. **Clone the repository**
   ```bash
   git clone https://github.com/kpoier/pastebin.git
   cd pastebin
   ```

2. **Configure Environment variables**
   Setup your `.env` to override defaults (Optional).
   ```env
   # .env
   ADMIN_URL_PREFIX=/manage
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=supersecretpassword
   HOST=0.0.0.0
   PORT=5000
   ```

3. **Deploy with Docker**
   ```bash
   docker-compose -f docker/docker-compose.yml up -d
   ```
   The application will be running directly on `http://127.0.0.1:5000`.

## Image Registry
Automatically built via GitHub Actions to Docker Hub:
`docker pull kpoier/pastebin:latest`

## License
MIT