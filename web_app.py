from flask import Flask, request, render_template
from twitter_api import fetch_user_data
from model import predict
import os
import logging

# Setup basic logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(
    __name__,
    template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "templates"))
)

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    username = None
    user_data = None

    if request.method == "POST":
        username = request.form["username"].strip()
        try:
            user_data = fetch_user_data(username)
            result = int(predict(user_data))
            prediction = "🟥 Fake" if result == 1 else "🟩 Genuine"
        except Exception as e:
            logging.error(f"Error for {username}: {str(e)}") # useful for debugging in terminal
            prediction = f"❌ Error: {str(e)}"

    return render_template("index.html", prediction=prediction, username=username, user_data=user_data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5050)))
