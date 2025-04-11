import pandas as pd
import os
import json
import time
from tweepy import Client, TooManyRequests

# ---- Setup ---- #
CACHE_FILE = "data/cache.json"
CACHE_PATH = "cached_users.json"
DATASET_PATH = "data/mock_users_dataset.csv"

# ✅ Ensure cache file exists and is valid
if not os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "w") as f:
        json.dump({}, f)

try:
    with open(CACHE_FILE, "r") as f:
        cache = json.load(f)
except json.JSONDecodeError:
    print("⚠️ Cache corrupted. Resetting.")
    cache = {}

# ✅ Load Twitter Bearer Token
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
if not BEARER_TOKEN:
    raise EnvironmentError("❌ Twitter Bearer Token not found in environment variables.")

client = Client(bearer_token=BEARER_TOKEN)

# ✅ Load CSV dataset
df = pd.read_csv(DATASET_PATH)

# ✅ Load or initialize JSON cache
if os.path.exists(CACHE_PATH):
    with open(CACHE_PATH, "r") as f:
        try:
            cache = json.load(f)
        except json.JSONDecodeError:
            print("⚠️ cached_users.json is corrupted. Resetting cache.")
            cache = {}
else:
    cache = {}

def save_cache():
    with open(CACHE_PATH, "w") as f:
        # Convert all numeric values to int for JSON compatibility
        safe_cache = {
            user: {k: int(v) if isinstance(v, (int, float)) else v for k, v in features.items()}
            for user, features in cache.items()
        }
        json.dump(safe_cache, f, indent=2)

def fetch_user_data(username):
    username = username.strip()

    if not username.isalnum() and "_" not in username:
        raise ValueError("❌ Invalid username format.")

    # 1. Check cache
    if username in cache:
        print(f"📦 Using cached data for {username}")
        return cache[username]

    # 2. Check CSV dataset
    if username in df["username"].values:
        print(f"📁 Found {username} in dataset.")
        user_row = df[df["username"] == username].iloc[0]
        user_data = {
            "followers_count": int(user_row["followers_count"]),
            "following_count": int(user_row["following_count"]),
            "tweet_count": int(user_row["tweet_count"]),
            "listed_count": int(user_row["listed_count"]),
            "verified": bool(user_row["verified"]),
            "has_profile_picture": bool(user_row["has_profile_picture"])
        }
        cache[username] = user_data
        save_cache()
        return user_data

    # 3. Fetch from Twitter API
    try:
        response = client.get_user(
            username=username,
            user_fields=["public_metrics", "verified", "profile_image_url"]
        )

        if response.data is None:
            raise ValueError(f"❌ User '{username}' not found on Twitter.")

        user = response.data
        metrics = user.public_metrics

        user_data = {
            "followers_count": int(metrics["followers_count"]),
            "following_count": int(metrics["following_count"]),
            "tweet_count": int(metrics["tweet_count"]),
            "listed_count": int(metrics["listed_count"]),
            "verified": bool(user.verified),
            "has_profile_picture": not user.profile_image_url.endswith("default_profile_normal.png")
        }

        # ✅ Update cache
        cache[username] = user_data
        save_cache()

        # ✅ Add to CSV dataset
        if username not in df["username"].values:
            new_row = {
                "username": username,
                "followers_count": user_data["followers_count"],
                "following_count": user_data["following_count"],
                "tweet_count": user_data["tweet_count"],
                "listed_count": user_data["listed_count"],
                "verified": int(user_data["verified"]),
                "has_profile_picture": int(user_data["has_profile_picture"])
            }
            df.loc[len(df)] = new_row
            df.to_csv(DATASET_PATH, index=False)
            print(f"✅ {username} added to dataset.")

        return user_data

    except TooManyRequests:
        raise RuntimeError("❌ Too many requests. Please try again later.")
    except Exception as e:
        raise RuntimeError(f"❌ Error fetching data for {username}: {e}")
