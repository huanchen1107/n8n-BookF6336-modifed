const API_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization=CWA-55FDA6D3-A43C-4AE0-BB30-E62D5F684FB2&elementName=平均溫度";

// Initialize Leaflet Map centered on Taiwan
const map = L.map('map', {
    zoomControl: false // Custom position
}).setView([23.6978, 120.9605], 8);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// Add zoom control to bottom right
L.control.zoom({
    position: 'bottomright'
}).addTo(map);

async function fetchWeatherData() {
    const loadingEl = document.getElementById('loading');
    try {
        loadingEl.classList.add('active');
        const response = await fetch(API_URL);
        const data = await response.json();
        
        const locations = data.records.Locations[0].Location;
        
        locations.forEach(loc => {
            const lat = parseFloat(loc.Latitude);
            const lon = parseFloat(loc.Longitude);
            const name = loc.LocationName;
            
            // Extract temperature data
            const tempElement = loc.WeatherElement.find(e => e.ElementName === "平均溫度") || loc.WeatherElement[0];
            
            if (lat && lon && tempElement) {
                // Generate Forecast HTML
                let forecastHtml = '';
                const timeSlots = tempElement.Time;
                
                // Show the next 5 time slots to keep popup clean
                const maxSlots = Math.min(5, timeSlots.length);
                
                for(let i=0; i<maxSlots; i++) {
                    const dateObj = new Date(timeSlots[i].StartTime);
                    // Format date (e.g. "Mon, 18:00")
                    const dateStr = dateObj.toLocaleDateString('zh-TW', { weekday: 'short', hour: '2-digit', minute:'2-digit' });
                    const temp = timeSlots[i].ElementValue[0].Temperature;
                    
                    forecastHtml += `
                        <div class="forecast-item">
                            <span class="forecast-date">${dateStr}</span>
                            <span class="forecast-temp">${temp}°C</span>
                        </div>
                    `;
                }

                const popupContent = `
                    <div class="weather-card">
                        <h3>${name}</h3>
                        <div class="forecast-list">
                            ${forecastHtml}
                        </div>
                    </div>
                `;

                // Add marker
                const marker = L.marker([lat, lon]).addTo(map);
                marker.bindPopup(popupContent);
            }
        });
        
    } catch (error) {
        console.error("Error fetching weather data:", error);
    } finally {
        loadingEl.classList.remove('active');
    }
}

// Start app
fetchWeatherData();
