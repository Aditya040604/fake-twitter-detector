# 🕵️‍♂️ Fake Twitter Account Detector

A Flask-based web app that predicts whether a Twitter account is **Fake** or **Genuine** using profile metadata and a trained **Random Forest** Machine Learning model.

## 🚀 Live Demo

> Coming soon — deploy to Render/Heroku and share your link here!

---

## 🧠 Features

- 🔍 Analyze Twitter usernames instantly
- 🤖 ML prediction: 🟥 **Fake** or 🟩 **Genuine**
- 🌐 Live Twitter API integration
- 💾 Data caching to reduce API calls
- 🧹 Clean Bootstrap UI
- 📈 Powered by **Random Forest Classifier**

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/aditya040604/fake-twitter-detector.git
cd fake-twitter-detector
```

### 2. Set Up Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Add Twitter API Token

```bash
export TWITTER_BEARER_TOKEN=your_token_here
```

---

## ▶️ Run the App

```bash
python src/web_app.py
```

Then open [http://127.0.0.1:5050](http://127.0.0.1:5050) in your browser.

---

## 🧠 Model Details

- **Algorithm:** Random Forest Classifier
- **Features Used:**
  - Follower count
  - Following count
  - Tweet count
  - Listed count
  - Account creation date
  - Bio description presence

You can enhance accuracy by training on a larger, more diverse dataset and fine-tuning hyperparameters.

---

## 🔐 Security Note

Sensitive tokens like `TWITTER_BEARER_TOKEN` should be stored securely in environment variables or `.env` files. Avoid committing them to version control.

---

## 👨‍💻 Author

Built by [Aditya](https://github.com/aditya040604) with 💻 and ☕
