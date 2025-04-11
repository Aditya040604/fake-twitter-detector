import joblib
import pandas as pd

# 👇 Define the function that can be imported
def predict(user_data):
    model = joblib.load("models/random_forest.pkl")

    # Convert user_data dict into a DataFrame
    df = pd.DataFrame([{
        "followers_count": user_data["followers_count"],
        "following_count": user_data["following_count"],
        "tweet_count": user_data["tweet_count"],
        "listed_count": user_data["listed_count"],
        "verified": int(user_data["verified"]),
        "has_profile_picture": int(user_data["has_profile_picture"])
    }])

    return model.predict(df)[0]  # returns 0 (genuine) or 1 (fake)
