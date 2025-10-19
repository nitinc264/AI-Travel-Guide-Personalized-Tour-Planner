# AI-Travel-Guide-Personalized-Tour-Planner
# 🧭 AI Travel Guide

> ✨ A lightweight AI-powered travel itinerary generator with real-time weather updates.  
> Powered by *Google Gemini API* 🧠 and *OpenWeatherMap* ☁ — built with *Flask, **HTML/CSS/JS*, and a clean two-page UI.

---

## 🌟 Features

- 🗺 *AI-Generated Itineraries* — Create detailed day-by-day travel plans based on destination, number of days, and user interests using the models.generateContent endpoint from Gemini.  
- 🌦 *Real-Time Weather Info* — Fetch and display current weather for the chosen city using *OpenWeatherMap API*.  
- 🧩 *Simple & Clean UI* — Two pages only:  
  - index.html: Build your trip itinerary  
  - suggestions.html: Get travel ideas & recommendations  
- 🔗 *CORS-Enabled Backend* — Smooth frontend-backend communication for easy local or hosted development.  

---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| *Backend* | Flask + Flask-CORS + Requests |
| *Frontend* | HTML, CSS, Vanilla JavaScript |
| *Weather API* | OpenWeatherMap (metric units) |
| *LLM API* | Google Gemini (models.generateContent) |

---


AI-Travel-Guide/
│
├── app.py # Flask server, routes, and Gemini/OpenWeather integration
├── list_models.py # Helper script to list available Gemini models
├── requirements.txt # Python dependencies
│
├── templates/
│ ├── index.html # Itinerary builder page
│ └── suggestions.html # Suggestions page
│
├── static/
│ ├── style.css # UI styling
│ └── script.js # Client-side API logic
│
└── .env.example # Example environment variables



---

## ⚙ Prerequisites

- 🐍 Python 3.x  
- 💡 virtualenv (recommended)  
- 🔑 API Keys for:
  - *Google Gemini* → GOOGLE_API_KEY
  - *OpenWeatherMap* → OPENWEATHER_API_KEY

---

## 🚀 Setup Instructions

### 1️⃣ Clone & Install Dependencies

```bash
git clone https://github.com/yourusername/ai-travel-guide.git
cd ai-travel-guide

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt


2️⃣ Configure Environment Variables

Copy .env.example → .env and fill in your keys:

GOOGLE_API_KEY=your_gemini_api_key
OPENWEATHER_API_KEY=your_openweather_key
MODEL_NAME=models/gemini-2.5-pro   # or gemini-2.5-flash


💡 Tip: Run python list_models.py to list supported models.
Make sure your MODEL_NAME supports generateContent.

3️⃣ Run the App Locally
python app.py


Then open your browser at:
👉 http://127.0.0.1:5000

You’ll see the itinerary builder UI with live weather integration! 🌍

🌐 API Endpoints
Method	Endpoint	Description
POST	/generate-itinerary	Generate AI-based itinerary (JSON: {destination, days, interests})
GET	/get-weather?city=CityName	Fetch current weather from OpenWeatherMap
GET	/	Render main itinerary builder page
GET	/suggestions	Render travel suggestions page
💻 Frontend Behavior

The user form collects destination, days, and interests.

JS (static/script.js) sends concurrent API calls for weather 🌦 and itinerary 🧳.

Responses are dynamically rendered into the DOM with loading indicators.

🧩 Troubleshooting
Issue	Cause	Fix
⚠ 404 model not found	Invalid model name	Run list_models.py → update .env with a valid Gemini model (supports generateContent)
🌤 Weather works but itinerary empty	Rendering issue	Check DOM update logic in script.js
🔒 CORS or mixed content error	Incorrect API base or missing CORS	Ensure Flask-CORS is enabled & frontend points to correct backend URL
🔒 Security Notes

❌ Never commit .env files — include only .env.example.

🛡 Add error handling and safe timeouts in production to prevent stack trace leaks.

🛣 Roadmap

🗃 Add persistent storage (SQLite/MongoDB) for saved trips.

✈ Enhance suggestions page with curated destinations.

📋 Add “Download Itinerary” and “Copy Plan” features.

📜 License

🪪 Licensed under the MIT License — feel free to use and modify!
See the LICENSE file for details.

💖 Acknowledgements

Google Gemini API

OpenWeatherMap API

Flask

🌍 Plan smarter. Travel lighter. Dream bigger. ✨

AI Travel Guide — your smart companion for every adventure.


---

Would you like me to generate the matching **LICENSE (MIT)** file content too, so your GitHub repo looks co
## 📁 Project Structure
