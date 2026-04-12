# Pastebin & File Host (Terminal Edition)

A fully self-hosted, extremely minimalist, and modern terminal-styled Pastebin and File Hosting server.

## Tech Stack
- **Backend:** Python, Flask, Gunicorn
- **Database:** SQLite, SQLAlchemy
- **Frontend:** HTML, Vanilla CSS, Vanilla JS
- **Infrastructure:** Docker, Docker Compose, GitHub Actions

## Deploy from Docker Hub (Recommended)

You can launch the server instantly using the pre-built image from Docker Hub.

1. **Create an environment file (Optional)**
   Setup a `.env` file to customize your admin credentials and routing:
   ```env
   ADMIN_URL_PREFIX=/manage
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=supersecretpassword
   HOST=0.0.0.0
   PORT=5000
   ```

2. **Run via Docker Run**
   Execute the following command to pull the latest image and mount the persistent folders (uploads & database) automatically:
   ```bash
   docker run -d \
     -p 5000:5000 \
     --env-file .env \
     -v $(pwd)/uploads:/app/uploads \
     -v $(pwd)/database.db:/app/database.db \
     --name pastebin \
     --restart always \
     kpoier/pastebin:latest
   ```
   The server will directly be available at `http://127.0.0.1:5000`.

## Local Build & Deployment

If you prefer to build the image yourself or run it directly from the python code:

1. **Clone the repository**
   ```bash
   git clone https://github.com/kpoier/pastebin.git
   cd pastebin
   ```

2. **Deploy with Docker Compose (Local Build)**
   ```bash
   docker-compose -f docker/docker-compose.yml up -d
   ```

3. **Deploy with Python (Development)**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r docker/requirements.txt
   python run.py
   ```

## License
MIT