from flask import Flask
import redis
from pymongo import MongoClient

app = Flask(__name__)

# Connect to Redis
r = redis.Redis(host="redis", port=6379)

# Connect to MongoDB with authentication
mongo_client = MongoClient("mongodb://cole:Nti2702@mongo:27017/mydatabase?authSource=admin")
mongo_db = mongo_client["mydatabase"]
visits_collection = mongo_db["visits"]

@app.route("/")
def home():
    count = r.incr("hits")
    visits_collection.insert_one({"visit_number": count})
    return f"This page has been visited {count} times. Visit data saved to MongoDB."

if __name__ == "__main__":
    app.run(host="0.0.0.0")
