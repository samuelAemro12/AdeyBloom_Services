import logging
import os
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI
import threading

# Load .env early so env vars are available when uvicorn imports this module
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="AdeyBloom AI Services")


@app.get("/", summary="Root endpoint to check service status")
async def root():
    return {"message": "Welcome to AdeyBloom AI Services API"}


from telegram_bot import create_application
from api.database import connect_to_mongo, close_mongo
from api import services as api_services
from api.routes_products import router as products_router

# Mount API routes
app.include_router(products_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    # Connect to MongoDB first (if configured)
    await connect_to_mongo(app)

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.warning("TELEGRAM_BOT_TOKEN not set; Telegram bot will not start.")
        return

    logger.info("Starting Telegram bot in background thread (polling)...")
    application = create_application(token)

    # Attach DB and services to the telegram Application so handlers can access them
    try:
        application.bot_data["db"] = app.state.db
        application.bot_data["services"] = api_services
    except Exception:
        logger.exception("Failed to attach DB/services to application.bot_data; continuing.")

    # Run blocking polling call in a daemon thread so FastAPI remains responsive
    t = threading.Thread(target=application.run_polling, daemon=True)
    t.start()
    app.state.bot_thread = t
    app.state.bot_app = application
    logger.info("Telegram bot thread started.")


@app.on_event("shutdown")
async def shutdown_event():
    bot_app = getattr(app.state, "bot_app", None)
    if bot_app:
        logger.info("Shutting down Telegram bot...")
        try:
            # stop() and shutdown() are async; await them to ensure graceful shutdown
            await bot_app.stop()
            await bot_app.shutdown()
        except Exception:
            logger.exception("Failed during bot shutdown; continuing exit.")
    # Close MongoDB connection (if any)
    try:
        await close_mongo(app)
    except Exception:
        logger.exception("Error while closing MongoDB connection during shutdown.")


def main():
    logger.info("Starting AdeyBloom Services API on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
