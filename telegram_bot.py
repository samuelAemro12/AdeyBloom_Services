import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# NOTE: `.env` is loaded by `main.py` (via `load_dotenv()`); avoid loading it here
# so imports remain side-effect free when uvicorn imports the module.

# Configure logging for the module
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# --- Callback Data Constants ---
BROWSE_PRODUCTS = "browse_products"
VIEW_CART = "view_cart"
TRACK_ORDER = "track_order"
AI_ASSISTANT = "ai_assistant"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a minimal welcome message."""
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("1️⃣ Browse Products", callback_data=BROWSE_PRODUCTS)],
        [InlineKeyboardButton("2️⃣ View Cart", callback_data=VIEW_CART)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_html(f"🌸 Welcome, {user.mention_html()}!", reply_markup=reply_markup)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == BROWSE_PRODUCTS:
        await query.edit_message_text(text="Feature coming soon: Browse Products")
    elif query.data == VIEW_CART:
        await query.edit_message_text(text="Feature coming soon: View Cart")
    else:
        await query.edit_message_text(text="Unknown option selected.")


def create_application(token: str) -> Application:
    """Build and return a telegram Application with minimal handlers.

    The function does not start the application; it only configures handlers.
    Caller is responsible for running `application.run_polling()`.
    """
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    logger.info("Telegram bot application created (handlers registered).")
    return application



