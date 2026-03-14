from flask import Flask, render_template, request, jsonify
import mysql.connector
import requests
import random
import datetime
import os
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

app = Flask(__name__)

# ─── Configuration ───────────────────────────────────────────────────────────
EXTERNAL_LOG_ENDPOINT = os.getenv("EXTERNAL_LOG_ENDPOINT", "http://localhost:8080")

DB_CONFIG = {
    "host":     os.getenv("DB_HOST",     "localhost"),
    "user":     os.getenv("DB_USER",     "root"),
    "password": os.getenv("DB_PASSWORD", "yourpassword"),
    "database": os.getenv("DB_NAME",     "activity_logs"),
}

DEMO_USERNAMES = [
    "alice_smith", "bob_jones", "carol_white", "david_lee",
    "emma_brown", "frank_wilson", "grace_taylor", "henry_davis",
    "demo_user", "admin_user",
]

SOURCE_IPS = [
    "192.168.1.10", "192.168.1.25", "10.0.0.5",
    "172.16.0.12",  "203.0.113.42",  "198.51.100.7",
]
# ─────────────────────────────────────────────────────────────────────────────


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


# ── Pages ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html",
                           endpoint=EXTERNAL_LOG_ENDPOINT)


@app.route("/generator")
def generator():
    return render_template("generator.html",
                           endpoint=EXTERNAL_LOG_ENDPOINT)


@app.route("/logs")
def logs_page():
    return render_template("logs.html")


@app.route("/architecture")
def architecture():
    return render_template("architecture.html",
                           endpoint=EXTERNAL_LOG_ENDPOINT)


# ── API ───────────────────────────────────────────────────────────────────────

@app.route("/api/generate_log", methods=["POST"])
def generate_log():
    data = request.get_json(silent=True) or {}

    username  = data.get("username",  random.choice(DEMO_USERNAMES))
    action    = data.get("action",    "login")
    source_ip = data.get("source_ip", random.choice(SOURCE_IPS))
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"

    # 1 ─ Save to MySQL
    db_status = "ok"
    db_error  = None
    try:
        conn   = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user_logs (username, action, source_ip) VALUES (%s, %s, %s)",
            (username, action, source_ip),
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        db_status = "error"
        db_error  = str(e)

    # 2 ─ Forward to external HTTP endpoint
    payload = {
        "username":  username,
        "action":    action,
        "source":    "web_app",
        "source_ip": source_ip,
        "timestamp": timestamp,
    }
    http_status = "ok"
    http_error  = None
    try:
        resp = requests.post(
            EXTERNAL_LOG_ENDPOINT,
            json=payload,
            timeout=3,
        )
        http_status = f"http_{resp.status_code}"
    except Exception as e:
        http_status = "error"
        http_error  = str(e)

    return jsonify({
        "success":     db_status == "ok",
        "event":       payload,
        "db_status":   db_status,
        "db_error":    db_error,
        "http_status": http_status,
        "http_error":  http_error,
    })


@app.route("/api/logs", methods=["GET"])
def get_logs():
    limit  = int(request.args.get("limit",  100))
    offset = int(request.args.get("offset", 0))
    try:
        conn   = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, username, action, source_ip, created_at "
            "FROM user_logs ORDER BY created_at DESC LIMIT %s OFFSET %s",
            (limit, offset),
        )
        rows = cursor.fetchall()
        cursor.execute("SELECT COUNT(*) AS total FROM user_logs")
        total = cursor.fetchone()["total"]
        cursor.close()
        conn.close()

        for row in rows:
            if hasattr(row["created_at"], "isoformat"):
                row["created_at"] = row["created_at"].isoformat()

        return jsonify({"logs": rows, "total": total, "success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e), "logs": [], "total": 0})


@app.route("/api/stats", methods=["GET"])
def get_stats():
    try:
        conn   = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) AS total FROM user_logs")
        total = cursor.fetchone()["total"]

        cursor.execute(
            "SELECT action, COUNT(*) AS count FROM user_logs GROUP BY action ORDER BY count DESC"
        )
        by_action = cursor.fetchall()

        cursor.execute(
            "SELECT DATE(created_at) AS day, COUNT(*) AS count "
            "FROM user_logs WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY) "
            "GROUP BY day ORDER BY day"
        )
        by_day = cursor.fetchall()
        for row in by_day:
            if hasattr(row["day"], "isoformat"):
                row["day"] = row["day"].isoformat()

        cursor.execute(
            "SELECT id, username, action, source_ip, created_at "
            "FROM user_logs ORDER BY created_at DESC LIMIT 5"
        )
        recent = cursor.fetchall()
        for row in recent:
            if hasattr(row["created_at"], "isoformat"):
                row["created_at"] = row["created_at"].isoformat()

        cursor.close()
        conn.close()

        return jsonify({
            "success":   True,
            "total":     total,
            "by_action": by_action,
            "by_day":    by_day,
            "recent":    recent,
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/api/config", methods=["GET"])
def get_config():
    return jsonify({"endpoint": EXTERNAL_LOG_ENDPOINT})


@app.route("/api/config/endpoint", methods=["POST"])
def update_endpoint():
    global EXTERNAL_LOG_ENDPOINT
    data = request.get_json(silent=True) or {}
    new_url = data.get("endpoint", "").strip()
    if new_url:
        EXTERNAL_LOG_ENDPOINT = new_url
        return jsonify({"success": True, "endpoint": EXTERNAL_LOG_ENDPOINT})
    return jsonify({"success": False, "error": "Empty endpoint"}), 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
