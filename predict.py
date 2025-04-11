import sys
from model import predict
from twitter_api import fetch_user_data
import csv
import datetime

CSV_FILE = "data/mock_users_dataset.csv"
USERNAME_TO_CHECK = sys.argv[1] if len(sys.argv) > 1 else "elonmusk"

# 🔸 Function to search for user in dataset
def find_user_in_dataset(username):
    try:
        with open(CSV_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"].lower() == username.lower():
                    print(f"📁 Found {username} in dataset.")
                    return {
                        "username": row["username"],
                        "followers_count": int(row["followers_count"]),
                        "following_count": int(row["following_count"]),
                        "tweet_count": int(row["tweet_count"]),
                        "listed_count": int(row["listed_count"]),
                        "verified": row["verified"].lower() == "true",
                        "has_profile_picture": row["has_profile_picture"].lower() == "true"
                    }
    except FileNotFoundError:
        print("❌ Dataset file not found.")
    return None

# 🔸 Function to log prediction results
def log_prediction(username, label):
    with open("logs/predictions_log.csv", "a") as f:
        timestamp = datetime.datetime.now().isoformat()
        f.write(f"{timestamp},{username},{label}\n")

# 🔸 Main logic
user_data = find_user_in_dataset(USERNAME_TO_CHECK)

if not user_data:
    print(f"🌐 {USERNAME_TO_CHECK} not in dataset, fetching from Twitter API...")
    user_data = fetch_user_data(USERNAME_TO_CHECK)

if user_data:
    result = predict(user_data)
    label = "Fake" if result else "Genuine"
    print(f"🧠 Prediction for {USERNAME_TO_CHECK}: {label}")
    log_prediction(USERNAME_TO_CHECK, label)
else:
    print(f"❌ Unable to get data for {USERNAME_TO_CHECK}")
