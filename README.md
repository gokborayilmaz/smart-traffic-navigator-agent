21-Day Agent Series: Day 10 AGENT : Smart Traffic Navigator Agent

Smart Traffic Navigator Agent
This agent is part of the "A New AI Agent Every Day!" Series - Day 10/21 - Smart Traffic Navigator Agent 🚦🚗✨ This AI agent analyzes real-time traffic density, suggests alternative routes, and estimates travel times using GoogleMaps MCP! 🗺️

## Installation

### Prerequisites
- Python 3.9 or higher
- Git
- Virtual environment (recommended)

### Steps
Don't forget to download nodejs for MCP

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and configure it as follows:

   ```env
   AZURE_OPENAI_ENDPOINT="your_azure_openai_endpoint"
   AZURE_OPENAI_API_VERSION="your_azure_openai_api_version"
   AZURE_OPENAI_API_KEY="your_azure_openai_api_key"
   GOOGLE_MAPS_API_KEY="YOUR_GOOGLE_MAPS_API_KEY"
   ```

## Running the Application

Start the FastAPI server:

```bash
uvicorn upsonicai:app --reload
```

Open the UI in your browser:

```
http://127.0.0.1:8000/
```

Use the form to input:
- Origin City
- Destination City

Click "Find Route" to analyze the best route, traffic conditions, and alternative paths. Results will be displayed dynamically.

## API Documentation
Interactive API docs are available at:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

