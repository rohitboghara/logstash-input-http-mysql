# ActivityLog — User Activity Monitor

A demo Flask web app that logs user events to MySQL and forwards them as JSON to a configurable external HTTP endpoint.

---

## Quick Start

### 1. Set up MySQL

```sql
mysql -u root -p < database.sql
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the app

Open `app.py` and set your values:

```python
EXTERNAL_LOG_ENDPOINT = "http://your-endpoint:8080"

DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "yourpassword",
    "database": "activity_logs",
}
```

Or use environment variables:

```bash
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=yourpassword
export DB_NAME=activity_logs
```

### 4. Run the app

```bash
python app.py
```

Open http://localhost:5000

---

## Pages

| URL            | Description                        |
|----------------|------------------------------------|
| `/`            | Landing page                       |
| `/dashboard`   | Live stats & charts                |
| `/generator`   | Click buttons to fire events       |
| `/logs`        | Paginated MySQL log table          |
| `/architecture`| Architecture & API reference       |

## API Endpoints

| Method | Path                    | Description                              |
|--------|-------------------------|------------------------------------------|
| POST   | `/api/generate_log`     | Create event → MySQL + HTTP forward      |
| GET    | `/api/logs`             | List log records (paginated)             |
| GET    | `/api/stats`            | Aggregate stats for dashboard            |
| GET    | `/api/config`           | Get current external endpoint URL        |
| POST   | `/api/config/endpoint`  | Update external endpoint URL at runtime  |

## JSON Event Payload

```json
{
  "username":  "alice_smith",
  "action":    "login",
  "source":    "web_app",
  "source_ip": "192.168.1.10",
  "timestamp": "2025-01-15T08:23:11Z"
}
```

## Project Structure

```
project/
├── app.py                  ← Flask backend
├── requirements.txt
├── database.sql            ← MySQL schema + seed data
├── templates/
│   ├── base.html           ← Shared sidebar layout
│   ├── index.html          ← Landing page
│   ├── dashboard.html      ← Stats dashboard
│   ├── generator.html      ← Event generator
│   ├── logs.html           ← MySQL log table
│   └── architecture.html   ← Architecture overview
└── static/
    ├── css/
    │   ├── style.css       ← Main dark theme
    │   └── landing.css     ← Landing page styles
    └── js/
        └── main.js         ← Sidebar + global helpers
```
