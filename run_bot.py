"""
DEPRECATED: `run_bot.py` removed from active workflow.

The Telegram bot is started by FastAPI on application startup (see `main.py`).
If you need a standalone runner for development, recreate one that calls
`create_application(token)` from `telegram_bot.py` and runs `application.run_polling()`.
"""
raise RuntimeError("run_bot.py is deprecated; start the service with `uvicorn main:app`")
