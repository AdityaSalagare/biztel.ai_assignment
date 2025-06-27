from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from summarizer import TranscriptAnalyzer
from data_pipeline import DataPreprocessor
import logging
import pandas as pd
from contextlib import asynccontextmanager
import os
import bugsnag
from bugsnag.asgi import BugsnagMiddleware
import ddtrace

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Biztel AI Analysis API",
    description="An API for analyzing and processing chat transcript data.",
    version="1.0.0"
)

# --- Pydantic Models ---
class TextInput(BaseModel):
    text: str

class PreprocessedText(BaseModel):
    original_text: str
    processed_text: str

class MessageCounts(BaseModel):
    agent_1: int
    agent_2: int

class OverallSentiments(BaseModel):
    agent_1: str
    agent_2: str

class AnalysisResult(BaseModel):
    transcript_id: str
    possible_article_link: str
    message_counts: MessageCounts
    overall_sentiments: OverallSentiments
    conversation_summary: str
    accuracy_report: str

# --- Global objects ---
# Load the analyzer at startup to avoid reloading the model on each request.
# This is a performance optimization.
try:
    analyzer = TranscriptAnalyzer('BiztelAI_DS_Dataset_V1.json')
    logger.info("TranscriptAnalyzer loaded successfully.")
except FileNotFoundError as e:
    logger.error(f"Failed to load data: {e}")
    analyzer = None

# --- Monitoring Setup ---

# Datadog Tracing
# Configure Datadog tracer. For this to work, you need to run the app with `dd-trace-run`.
# Environment variables like DD_ENV, DD_SERVICE, DD_VERSION, DD_API_KEY will be used.
ddtrace.configure(
    fastapi=True,
    # Add any other integrations you need
)

# Bugsnag Error Monitoring
# Configure Bugsnag with your API key from an environment variable.
if os.getenv("BUGSNAG_API_KEY"):
    bugsnag.configure(
        api_key=os.getenv("BUGSNAG_API_KEY"),
        project_root="/app",  # Adjust if your project root is different in Docker
    )
    # Add Bugsnag middleware to the app
    app.add_middleware(BugsnagMiddleware)

# --- API Key Authentication ---
API_KEY = os.getenv("API_KEY", "AdityaSalagare")  # Use env var or default
API_KEY_NAME = "X-API-Key"

def api_key_auth(x_api_key: str = Header(..., alias=API_KEY_NAME)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key.")

# --- API Endpoints ---

# @app.on_event("startup")
# async def startup_event():
#     if analyzer is None:
#         # This will prevent the app from starting if the data file is not found.
#         raise RuntimeError("Failed to initialize TranscriptAnalyzer. Check if the data file exists.")
@asynccontextmanager
async def lifespan(app: FastAPI):
    if analyzer is None:
        raise RuntimeError("Failed to initialize TranscriptAnalyzer. Check if the data file exists.")
    yield

app = FastAPI(
    title="Biztel AI Analysis API",
    description="An API for analyzing and processing chat transcript data.",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def read_root():
    # A welcome message to verify the API is running.
    return {"message": "Welcome to the Biztel AI Analysis API!"}


@app.get("/summary", summary="Get Dataset Summary")
async def get_dataset_summary(api_key: str = Depends(api_key_auth)):
    # Endpoint 1: Fetches and returns a processed dataset summary.
    # This endpoint is defined as async to maintain consistency and allow
    # for potentially long-running operations.
    if analyzer is None:
        raise HTTPException(status_code=500, detail="Analyzer not initialized.")
        
    df = analyzer.df
    
    summary = {
        "total_transcripts": df['transcript_id'].nunique(),
        "total_messages": len(df),
        "messages_per_agent": df['agent'].value_counts().to_dict(),
        "sentiment_distribution": df['sentiment'].value_counts().to_dict(),
        "turn_rating_distribution": df['turn_rating'].value_counts().to_dict()
    }
    
    return summary

@app.post("/transform", response_model=PreprocessedText, summary="Preprocess Raw Text")
async def transform_text(text_input: TextInput, api_key: str = Depends(api_key_auth)):
    # Endpoint 2: Performs real-time data transformation.
    # Takes raw text and returns a preprocessed version.
    # This function is async to prevent blocking the server's event loop.
    # While the ML model inference in `transform_text` is CPU-bound, FastAPI
    # runs synchronous functions in a separate thread pool by default. Defining
    # this as `async` makes the non-blocking behavior more explicit and is a best
    # practice for potentially long-running operations.
    # We can instantiate a preprocessor on the fly as it has no heavy components.
    # We pass a dummy dataframe to initialize it.
    preprocessor = DataPreprocessor(pd.DataFrame()) 
    processed_text = preprocessor.preprocess_text(text_input.text)
    
    return {
        "original_text": text_input.text,
        "processed_text": processed_text
    }

@app.get("/analyze-transcript/{transcript_id}", response_model=AnalysisResult, summary="Analyze a Transcript")
async def analyze_transcript(transcript_id: str, api_key: str = Depends(api_key_auth)):
    # Endpoint 3: Allows users to send a transcript ID and receive processed insights.
    # This function is async to prevent blocking the server's event loop.
    # While the ML model inference in `analyze_transcript` is CPU-bound, FastAPI
    # runs synchronous functions in a separate thread pool by default. Defining
    # this as `async` makes the non-blocking behavior more explicit and is a best
    # practice for potentially long-running operations.
    if analyzer is None:
        raise HTTPException(status_code=500, detail="Analyzer not initialized.")
    
    result = analyzer.analyze_transcript(transcript_id)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
        
    return result

# if __name__ == "__main__":
#     import uvicorn
#     # To run this app, use the command: uvicorn main:app --reload
#     uvicorn.run(app, host="0.0.0.0", port=8000) 