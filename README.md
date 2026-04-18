# Stage 0 - Gender Classification API

A REST API built with FastAPI that predicts gender from a name using the Genderize API.

## Tech Stack
- Python
- FastAPI
- httpx

## Running Locally

1. Clone the repository
   git clone <https://github.com/Carrinson/Stage_0-HNG.git>

2. Install dependencies
   uv pip install -r requirements.txt

3. Start the server
   uvicorn main:app --reload

4. Visit http://localhost:8000/docs to test the endpoint

## API Usage

GET /api/classify?name=john

Response:
{
  "status": "success",
  "data": {
    "name": "john",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-01T12:00:00Z"
  }
}

## Live API
<https://stage0-hng-production.up.railway.app/>