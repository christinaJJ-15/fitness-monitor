from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["fitness_monitor"]
users_collection = db["users"]
bodydata_collection = db["body_data"]
progress_collection = db["progress"]

# Registration endpoint
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    if users_collection.find_one({"email": email}):
        return jsonify({"status": "error", "message": "❌ Email already exists."})
    users_collection.insert_one({
        "name": data.get("name"),
        "email": email,
        "password": data.get("password")
    })
    return jsonify({"status": "success", "message": "✅ Registered successfully!"})

# Login endpoint
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = users_collection.find_one({
        "email": data.get("email"),
        "password": data.get("password")
    })
    if user:
        return jsonify({"status": "success", "message": f"✅ Welcome, {user['name']}!"})
    else:
        return jsonify({"status": "error", "message": "❌ Invalid credentials!"})

# Body condition saving endpoint
@app.route("/bodydata", methods=["POST"])
def save_body_data():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "Empty data!"})
    bodydata_collection.insert_one(data)
    return jsonify({"status": "success", "message": "✅ Body data saved!"})

# Save daily/weekly progress
@app.route("/save_progress", methods=["POST"])
def save_progress():
    data = request.json
    if not data.get("email"):
        return jsonify({"status": "error", "message": "Email missing."})
    data["timestamp"] = datetime.utcnow()
    progress_collection.insert_one(data)
    return jsonify({"status": "success", "message": "✅ Progress saved!"})

# View progress for the current user
@app.route("/view_progress", methods=["POST"])
def view_progress():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"status": "error", "message": "Email is required"}), 400

    progress = list(progress_collection.find({"email": email}))

    for p in progress:
        p["_id"] = str(p["_id"])  # Convert ObjectId to string

    return jsonify({"status": "success", "data": progress})

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
