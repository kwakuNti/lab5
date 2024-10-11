from flask import Flask, jsonify, render_template_string
import redis
import psycopg2

app = Flask(__name__)

# Connect to Redis
redis_client = redis.StrictRedis(host='redis', port=6379, decode_responses=True)

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        host="localhost",
        database="lab5",
        user="root",
        password="Nti2702."
        port=5432  # Change this to 5433 if you updated the docker-compose file

    )
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS visitors (id SERIAL PRIMARY KEY, visit_count INT);")
    cur.execute("INSERT INTO visitors (visit_count) VALUES (1);")
    conn.commit()
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error connecting to PostgreSQL: {e}")

@app.route('/')
def index():
    # Connect to PostgreSQL to fetch data
    conn = psycopg2.connect(
        host="db",
        database="postgres_db",
        user="postgres",
        password="password"
    )
    cur = conn.cursor()
    cur.execute("SELECT visit_count FROM visitors ORDER BY id DESC LIMIT 1;")
    visit_count = cur.fetchone()[0]
    cur.close()
    conn.close()

    # HTML response with embedded CSS
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flask Visitor Counter</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                color: #333;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .container {{
                text-align: center;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                font-size: 2em;
                margin-bottom: 10px;
            }}
            p {{
                font-size: 1.2em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to Flask!</h1>
            <p>Visit Count: <strong>{visit_count}</strong></p>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
