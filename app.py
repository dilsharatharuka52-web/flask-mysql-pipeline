from flask import Flask, jsonify, request
import mysql.connector
import os
import time

app = Flask(__name__)

def get_db_connection():
    """Create a database connection using environment variables"""
    retries = 5
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host=os.environ.get('MYSQL_HOST', 'mysql'),
                user=os.environ.get('MYSQL_USER', 'root'),
                password=os.environ.get('MYSQL_PASSWORD', 'root'),
                database=os.environ.get('MYSQL_DB', 'devops')
            )
            return conn
        except mysql.connector.Error:
            retries -= 1
            time.sleep(3)
    return None

@app.route('/')
def index():
    """Home page — tests DB connection"""
    conn = get_db_connection()
    if conn:
        conn.close()
        return jsonify({
            "status": "success",
            "message": "Two-tier Flask app is running!",
            "database": "connected"
        })
    return jsonify({"status": "error", "message": "Database not connected"}), 500

@app.route('/health')
def health():
    """Health check endpoint — used by Docker healthcheck"""
    return jsonify({"status": "healthy"}), 200

@app.route('/data', methods=['GET'])
def get_data():
    """Read records from the database"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM records")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

@app.route('/data', methods=['POST'])
def add_data():
    """Write a new record to the database"""
    data = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 500
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO records (name, value) VALUES (%s, %s)",
        (data.get('name'), data.get('value'))
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Record inserted"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)