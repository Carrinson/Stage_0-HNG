from fastapi import FastAPI, HTTPException, Request  # pyright: ignore[reportMissingImports]
from fastapi.responses import JSONResponse  # pyright: ignore[reportMissingImports]
import httpx   # pyright: ignore[reportMissingImports]
from fastapi.middleware.cors import CORSMiddleware  # pyright: ignore[reportMissingImports]
from datetime import datetime, timezone


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail
        }
    )


@app.get("/")
def read_root():
    return {"message": "Hello from stage-0!"}

@app.get("/api/classify")
async def classify(name: str):
    if not name.strip():
        raise HTTPException(status_code=400, detail="Empty input Enter a name")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api.genderize.io?name={name}")
            data = response.json()

            sample_size = data["count"]
            gender = data["gender"]
            probability = data["probability"]

            if gender is None or sample_size <= 0:
                raise HTTPException(status_code=404, detail="No prediction available for the provided name")
            is_confident = probability >= 0.7 and sample_size>= 100
            processed_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

            return {
                "status": "success",
                "data": {
                    "name":name,
                    "gender":gender,
                    "sample_size":sample_size,
                    "probability":probability,
                    "is_confident":is_confident,
                    "processed_at":processed_at,
                }
            }
    except httpx.RequestError: 
        raise HTTPException(status_code=502, detail="Bad Gateway") 











