from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from upsonic import Agent, Task, ObjectResponse
import os
from dotenv import load_dotenv

# .env dosyasını yükleyelim
load_dotenv()

app = FastAPI(title="Smart Traffic Navigator")

# 🚀 **AI Ajanını Başlat**
traffic_agent = Agent("Smart Traffic Navigator", model="azure/gpt-4o", reflection=True)

# 📌 Google Maps MCP Tanımlama
class GoogleMapsMCP:
    command = "npx"
    args = ["-y", "@modelcontextprotocol/server-google-maps"]
    env = {"GOOGLE_MAPS_API_KEY": os.getenv("GOOGLE_MAPS_API_KEY")}

# 📌 Yanıt Formatı
class RouteResponse(ObjectResponse):
    origin: str
    destination: str
    distance: str
    duration: str
    traffic_condition: str
    alternative_routes: list[str]

# 📌 API Endpoint: Trafik Rota Analizi
@app.get("/get_route")
async def get_route(origin: str, destination: str):
    route_description = f"""
    Find the best route between {origin} and {destination} by analyzing traffic density.
    Provide the total distance, estimated duration, traffic condition, and alternative routes.
    """

    route_task = Task(
        route_description,
        tools=[GoogleMapsMCP],
        response_format=RouteResponse
    )

    traffic_agent.do(route_task)
    route_data = route_task.response

    if not route_data:
        return {"error": "Failed to find the best route."}

    return {
        "origin": route_data.origin,
        "destination": route_data.destination,
        "distance": route_data.distance,
        "duration": route_data.duration,
        "traffic_condition": route_data.traffic_condition,
        "alternative_routes": route_data.alternative_routes
    }

# 📌 HTML + JavaScript UI Sayfası
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Smart Traffic Navigator</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100 flex justify-center items-center h-screen">
    
        <div class="bg-white p-8 rounded-lg shadow-lg w-96">
            <h1 class="text-2xl font-bold text-center mb-4">🚦 Smart Traffic Navigator</h1>
            
            <input id="origin" type="text" placeholder="Starting Location" class="w-full p-2 border rounded mb-2">
            <input id="destination" type="text" placeholder="Destination" class="w-full p-2 border rounded mb-4">
            
            <button onclick="getRoute()" class="bg-blue-500 text-white px-4 py-2 rounded w-full">Find Route</button>
    
            <div id="result" class="mt-4 text-sm"></div>
        </div>
    
        <script>
            async function getRoute() {
                const origin = document.getElementById("origin").value;
                const destination = document.getElementById("destination").value;
                if (!origin || !destination) {
                    alert("Please enter both locations.");
                    return;
                }
    
                const response = await fetch(`/get_route?origin=${origin}&destination=${destination}`);
                const data = await response.json();
    
                if (data.error) {
                    document.getElementById("result").innerHTML = `<p class='text-red-500'>Error: ${data.error}</p>`;
                    return;
                }
    
                document.getElementById("result").innerHTML = `
                    <p><strong>From:</strong> ${data.origin}</p>
                    <p><strong>To:</strong> ${data.destination}</p>
                    <p><strong>Distance:</strong> ${data.distance}</p>
                    <p><strong>Duration:</strong> ${data.duration}</p>
                    <p><strong>Traffic:</strong> ${data.traffic_condition}</p>
                    <p><strong>Alternative Routes:</strong></p>
                    <ul>${data.alternative_routes.map(route => `<li>${route}</li>`).join('')}</ul>
                `;
            }
        </script>
    
    </body>
    </html>
    """
