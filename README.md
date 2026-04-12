# Pastebin & File Host (Terminal Edition)

A fully self-hosted, extremely minimalist, and modern terminal-styled Pastebin and File Hosting server. Built with robust backend capabilities to securely manage text snippets and single files.

## High-Performance Features
- **Pure Native Output**: Paste links return 100% pure text or raw files directly (no HTML bloat) unless password protected.
- **Hardened Admin Dashboard**: Hidden route to manage all objects via a dense, native JS-powered data grid with instant search and sort.
- **Trash Retention System**: Deleted and expired pastes persist in a `[ TRASHED ]` state for 1 week before the internal cleanup daemon purges them from disk permanently.
- **Lifespan Control**: Allow granular TTL for your uploads, ranging from 10 minutes to maximum 2 weeks. Admins can bypass this and make files `[ PERMANENT ]`.
- **Hacker Aesthetic**: Monospace 'JetBrains Mono', pitch black cards, strict sharp corners, and highly responsive. RWD equipped.

## Getting Started

### Option 1: Docker (Recommended)
This repo comes out of the box with Docker Compose for a frictionless production-ready environment using `gunicorn`:

```bash
git clone <repository-url>
cd pastebin
docker-compose -f docker/docker-compose.yml up -d --build
```
Your instance will be running directly on `http://127.0.0.1:5000` with the database and uploads persistently bound to the host folders.

### Option 2: Local Python Environment
```bash
python -m venv venv
venv\Scripts\activate
pip install -r docker/requirements.txt
python run.py
```

## Security & Admin Instructions
All configuration is found in `config.py`.
- Change `ADMIN_URL_PREFIX` to disguise your admin panel (default: `/manage`)
- Change `ADMIN_USERNAME` and `ADMIN_PASSWORD` (default: `admin` / `supersecretpassword`)
- Uploads size are natively constrained to 25MB (modify `MAX_CONTENT_LENGTH` to alter this limit).

## License
MIT