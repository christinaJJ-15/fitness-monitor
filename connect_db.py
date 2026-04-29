from pymongo import MongoClient

# Step 1: Connect to local MongoDB server
client = MongoClient("mongodb://localhost:27017/")

# Step 2: Create/Get the database
db = client["fitness_monitor_db"]

# Step 3: Create/Get a collection
collection = db["users"]

# Step 4: Insert sample data
sample_user = {
    "name": "Christina",
    "email": "christina@example.com",
    "age": 22,
    "fitness_goal": "Weight Loss",
    "height_cm": 162,
    "weight_kg": 64,
    "allergies": ["milk", "nuts"]
}

# Insert the user
inserted = collection.insert_one(sample_user)

print("✅ Data inserted with ID:", inserted.inserted_id)
