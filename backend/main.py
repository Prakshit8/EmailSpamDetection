"""
FastAPI Backend for Email Fraud Detection System

This module provides a REST API endpoint for email fraud prediction
using a trained machine learning model.
"""

import pickle
import nltk
import string
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from typing import Dict, Any
import logging
from functools import lru_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="FraudShield AI - Email Fraud Detection API",
    description="Production-ready API for detecting email fraud and spam using machine learning",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request/response
class EmailRequest(BaseModel):
    email_text: str

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    processing_time_ms: float

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str

# Global variables for model components
model = None
vectorizer = None
stemmer = None
stop_words = None

def ensure_nltk_resource(resource_name: str) -> None:
    """Download NLTK resource if not already present."""
    try:
        nltk.data.find(resource_name)
    except LookupError:
        logger.info(f"Downloading NLTK resource: {resource_name}")
        nltk.download(resource_name.split('/')[-1], quiet=True)

def initialize_text_processing():
    """Initialize text processing components."""
    global stemmer, stop_words
    
    # Ensure NLTK resources are available
    ensure_nltk_resource('corpora/stopwords')
    ensure_nltk_resource('tokenizers/punkt')
    try:
        ensure_nltk_resource('tokenizers/punkt_tab')
    except Exception:
        pass
    
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    logger.info("Text processing components initialized")

def load_model_artifacts():
    """Load model and vectorizer with error handling."""
    global model, vectorizer
    
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        
        logger.info("Model and vectorizer loaded successfully")
        return True
    except FileNotFoundError as e:
        logger.error(f"Model artifacts not found: {e}")
        return False
    except Exception as e:
        logger.error(f"Failed to load model artifacts: {e}")
        return False

def transform_text(text: str) -> str:
    """
    Preprocess input text with comprehensive cleaning.
    
    Args:
        text: Input text to preprocess
    
    Returns:
        Cleaned and preprocessed text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Tokenize
    tokens = nltk.word_tokenize(text)
    
    # Remove non-alphanumeric characters
    tokens = [token for token in tokens if token.isalnum()]
    
    # Remove stopwords and punctuation
    tokens = [token for token in tokens if token not in stop_words and token not in string.punctuation]
    
    # Apply stemming
    tokens = [stemmer.stem(token) for token in tokens]
    
    return " ".join(tokens)

@lru_cache(maxsize=1000)
def predict_email_fraud_cached(email_text: str) -> tuple:
    """
    Make prediction with caching for performance.
    
    Args:
        email_text: Input email text
    
    Returns:
        Tuple of (prediction, confidence)
    """
    # Preprocess text
    cleaned_text = transform_text(email_text)
    
    # Vectorize
    vector_input = vectorizer.transform([cleaned_text]).toarray()
    
    # Get prediction and probability
    prediction = model.predict(vector_input)[0]
    
    # Get confidence score
    if hasattr(model, 'predict_proba'):
        probabilities = model.predict_proba(vector_input)[0]
        confidence = max(probabilities) * 100
    else:
        confidence = 85.0  # Default confidence if predict_proba not available
    
    return prediction, confidence

@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup."""
    logger.info("Starting FraudShield AI API...")
    
    # Initialize text processing
    initialize_text_processing()
    
    # Load model artifacts
    if not load_model_artifacts():
        logger.error("Failed to initialize model artifacts. API will not function properly.")
    
    logger.info("FraudShield AI API startup complete")

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with API health status."""
    return HealthResponse(
        status="healthy",
        model_loaded=model is not None and vectorizer is not None,
        version="1.0.0"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        model_loaded=model is not None and vectorizer is not None,
        version="1.0.0"
    )

@app.post("/predict", response_model=PredictionResponse)
async def predict_email(request: EmailRequest):
    """
    Predict whether an email is spam/fraud or safe.
    
    Args:
        request: EmailRequest containing email_text
    
    Returns:
        PredictionResponse with prediction and confidence
    """
    import time
    start_time = time.time()
    
    # Validate input
    if not request.email_text or not request.email_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Email text cannot be empty"
        )
    
    # Check if model is loaded
    if model is None or vectorizer is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please try again later."
        )
    
    try:
        # Make prediction
        prediction, confidence = predict_email_fraud_cached(request.email_text)
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Map prediction to human-readable format
        prediction_label = "Spam" if prediction == 1 else "Safe"
        
        logger.info(f"Prediction completed: {prediction_label} with {confidence:.2f}% confidence")
        
        return PredictionResponse(
            prediction=prediction_label,
            confidence=round(confidence, 2),
            processing_time_ms=round(processing_time, 2)
        )
        
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

@app.get("/stats")
async def get_model_stats():
    """Get model statistics and information."""
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded"
        )
    
    model_type = type(model).__name__
    
    return {
        "model_type": model_type,
        "vectorizer_type": "TF-IDF",
        "algorithm": model_type,
        "status": "active",
        "cache_enabled": True,
        "max_cache_size": 1000
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
