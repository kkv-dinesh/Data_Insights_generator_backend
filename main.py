from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import analysis
#from backend.api import analysis  # Import the router
from dotenv import load_dotenv
import os

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Initialize FastAPI
app = FastAPI(
    title="Multimeta.ai Data Insights Generator",
    description="Web application for automated dataset analysis and AI-driven insights."
)

# CORS configuration (React frontend)
origins = [
    "http://localhost:3000", 
    "https://data-insights-generator-frontend.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(analysis.router, prefix="/api/v1/data", tags=["data-analysis"])

@app.get("/")
def read_root():
    return {"message": "Backend is running. Use /api/v1/data/upload to POST a dataset."}
