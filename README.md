# Pastebin Clone

A simple, self-hosted pastebin clone built with Flask and SQLite.

## Features

- Create and view text pastes
- Automatic URL shortening
- Syntax highlighting (via Prism.js)
- Simple, clean interface

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pastebin
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

The application will be available at `http://[IP_ADDRESS]`.

## Usage

1. Open `http://[IP_ADDRESS]` in your browser
2. Enter your text in the textarea
3. Click **Create Paste**
4. Copy the generated URL to share your paste

## License

MIT