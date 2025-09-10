import logging
import uvicorn
from fastapi import FastAPI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="AdeyBloom AI Services")


@app.get("/", summary="Root endpoint to check service status")
async def root():
    """Returns a welcome message indicating the API is running."""
    return {"message": "Welcome to AdeyBloom AI Services API"}


def main():
    """Starts the uvicorn server for the FastAPI application."""
    logger.info("Starting AdeyBloom Services API on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
