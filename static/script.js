// static/script.js
document.addEventListener('DOMContentLoaded', () => {
  // Use same-origin for all API calls so it works locally and on Render
  const API_BASE_URL = ""; // keep empty to use current origin

  // --- Itinerary Builder Page Logic ---
  const itineraryForm = document.getElementById('itinerary-form');
  if (itineraryForm) {
    const loader = document.getElementById('loader');
    const resultsDiv = document.getElementById('results');
    const weatherInfoDiv = document.getElementById('weather-info');
    const itineraryOutputDiv = document.getElementById('itinerary-output');

    itineraryForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      // Get form data
      const destination = document.getElementById('destination').value.trim();
      const days = document.getElementById('days').value;
      const interests = document.getElementById('interests').value.trim();

      // Show loader and hide previous results
      loader.classList.remove('hidden');
      resultsDiv.classList.add('hidden');
      weatherInfoDiv.innerHTML = '';
      itineraryOutputDiv.innerHTML = '';

      try {
        // Fetch both weather and itinerary concurrently
        const [weatherResponse, itineraryResponse] = await Promise.all([
          fetch(`${API_BASE_URL}/get-weather?city=${encodeURIComponent(destination)}`),
          fetch(`${API_BASE_URL}/generate-itinerary`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ destination, days, interests })
          })
        ]);

        // Handle weather data
        if (weatherResponse.ok) {
          const weatherData = await weatherResponse.json();
          displayWeather(weatherData);
        } else {
          weatherInfoDiv.innerHTML = `<p>Could not fetch weather data.</p>`;
        }

        // Handle itinerary data
        if (itineraryResponse.ok) {
          const itineraryData = await itineraryResponse.json();
          // Use the 'marked' library to convert Markdown to HTML
          itineraryOutputDiv.innerHTML = marked.parse(itineraryData.itinerary || '');
        } else {
          itineraryOutputDiv.innerHTML = `<p>Error generating itinerary. Please try again.</p>`;
        }
      } catch (error) {
        console.error('Error:', error);
        itineraryOutputDiv.innerHTML = `<p>An unexpected error occurred. Please check the console.</p>`;
      } finally {
        // Hide loader and show results
        loader.classList.add('hidden');
        resultsDiv.classList.remove('hidden');
      }
    });

    function displayWeather(data) {
      if (data && data.main && data.weather && data.weather[0]) {
        const temp = data.main.temp;
        const description = data.weather[0].description;
        const icon = data.weather[0].icon;
        weatherInfoDiv.innerHTML = `
          <strong>Current weather in ${data.name}:</strong>
          ${temp}°C, ${description}.
          <img src="http://openweathermap.org/img/wn/${icon}.png"
               alt="weather icon"
               style="vertical-align: middle; width: 40px;">
        `;
      } else {
        weatherInfoDiv.innerHTML = `<p>Weather data unavailable.</p>`;
      }
    }
  }

  // --- Suggested Trips Page Logic ---
  const loadSuggestionsBtn = document.getElementById('load-suggestions-btn');
  if (loadSuggestionsBtn) {
    const loader = document.getElementById('loader');
    const suggestionsOutputDiv = document.getElementById('suggestions-output');

    loadSuggestionsBtn.addEventListener('click', async () => {
      loader.classList.remove('hidden');
      suggestionsOutputDiv.innerHTML = '';

      try {
        const response = await fetch(`${API_BASE_URL}/suggest-trips`);
        if (response.ok) {
          const data = await response.json();
          suggestionsOutputDiv.innerHTML = marked.parse(data.suggestions || '');
        } else {
          suggestionsOutputDiv.innerHTML = `<p>Error fetching suggestions. Please try again.</p>`;
        }
      } catch (error) {
        console.error('Error:', error);
        suggestionsOutputDiv.innerHTML = `<p>An unexpected error occurred.</p>`;
      } finally {
        loader.classList.add('hidden');
      }
    });
  }
});
