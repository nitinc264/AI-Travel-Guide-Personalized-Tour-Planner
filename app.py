import os
import requests
import time
import random
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

# --- Basic Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

# --- API Key and Model Configuration ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Use a v1-supported model by default; override via .env MODEL_NAME if desired.
# From your list_models output, these support generateContent:
#   models/gemini-2.5-flash, models/gemini-2.5-pro, models/gemini-2.0-flash, etc.
MODEL_NAME = os.getenv("MODEL_NAME", "models/gemini-2.5-flash")

# --- Flask App Initialization ---
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# --- Helper function to extract text ---
def _extract_text_from_response(j):
    try:
        return j["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError) as e:
        logger.error("Could not extract text from response: %s", j)
        raise RuntimeError(f"Unexpected API response format: {j}") from e

# --- AI Content Generation Function ---
def generate_ai_content(prompt, model=None, key=None, max_output_tokens=2048, attempts=3):
    model = model or MODEL_NAME
    key = key or GOOGLE_API_KEY
    if not key:
        raise RuntimeError("GOOGLE_API_KEY not set")

    url = f"https://generativelanguage.googleapis.com/v1/{model}:generateContent?key={key}"
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}],
            }
        ],
        "generationConfig": {
            "maxOutputTokens": max_output_tokens,
            "temperature": 0.7,
        },
    }

    backoff = 1.0
    for attempt in range(1, attempts + 1):
        try:
            logger.info("Generative API attempt %d: url=%s", attempt, url)
            resp = requests.post(url, headers=headers, json=body, timeout=120)
            resp.raise_for_status()
            j = resp.json()
            return _extract_text_from_response(j)
        except requests.exceptions.HTTPError as e:
            status = getattr(e.response, "status_code", None)
            text = getattr(e.response, "text", "")
            logger.error("HTTP error from Generative API status=%s text=%s", status, text)
            raise RuntimeError(f"Generative API HTTP error: {status} - {text}") from e
        except Exception as e:
            logger.exception("Unexpected error calling Generative API on attempt %d", attempt)
            if attempt == attempts:
                raise
            sleep_for = backoff + random.uniform(0, 0.5)
            logger.info("Sleeping %.1fs before retry", sleep_for)
            time.sleep(sleep_for)
            backoff *= 2.0

# --- API ENDPOINTS ---
@app.route('/generate-itinerary', methods=['POST'])
def generate_itinerary():
    try:
        data = request.json
        destination = data.get('destination')
        days = data.get('days')
        interests = data.get('interests')

        if not all([destination, days, interests]):
            return jsonify({"error": "Missing required fields"}), 400

        prompt = (
            f"Create a detailed, day-by-day travel itinerary for a trip to {destination} "
            f"for {days} days. The traveler is interested in {interests}. "
            f"Format the output in clean Markdown."
        )
        generated_text = generate_ai_content(prompt)
        return jsonify({"itinerary": generated_text})
    except Exception as e:
        logger.error("Error in /generate-itinerary: %s", e)
        return jsonify({"error": str(e)}), 500

@app.route('/get-weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logger.error("Error in /get-weather: %s", e)
        return jsonify({"error": f"Could not fetch weather data: {e}"}), 500

@app.route('/suggest-trips', methods=['GET'])
def suggest_trips():
    try:
        prompt = (
            "Suggest 5 interesting and diverse travel destinations. For each destination, "
            "provide: the name, a one-sentence highlight, and the best time to travel. "
            "Format as a Markdown list."
        )
        generated_text = generate_ai_content(prompt)
        return jsonify({"suggestions": generated_text})
    except Exception as e:
        logger.error("Error in /suggest-trips: %s", e)
        return jsonify({"error": str(e)}), 500

# --- Routes to serve HTML ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/suggestions')
def suggestions():
    return render_template('suggestions.html')

# --- Main entry point ---
if __name__ == '__main__':
    logger.info("Starting AI Travel Guide Flask app")
    app.run(debug=True, port=5000)
