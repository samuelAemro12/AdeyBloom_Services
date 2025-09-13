import logging
import os

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get the bot token from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables")

# --- Callback Data Constants ---
BROWSE_PRODUCTS = "browse_products"
VIEW_CART = "view_cart"
TRACK_ORDER = "track_order"
AI_ASSISTANT = "ai_assistant"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message with the main menu keyboard."""
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton("1️⃣ Browse Products", callback_data=BROWSE_PRODUCTS)],
        [InlineKeyboardButton("2️⃣ View Cart", callback_data=VIEW_CART)],
        [InlineKeyboardButton("3️⃣ Track My Order", callback_data=TRACK_ORDER)],
        [InlineKeyboardButton("4️⃣ Talk to AI Assistant 💬", callback_data=AI_ASSISTANT)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_message = (
        f"🌸 Welcome to AdeyBloom, {user.mention_html()}!\n"
        "Your beauty & self-care companion.\n\n"
        "What would you like to do today?"
    )
    
    await update.message.reply_html(welcome_message, reply_markup=reply_markup)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and calls the appropriate handler."""
    query = update.callback_query
    await query.answer()  # Acknowledge the button press

    # --- Placeholder logic for each button ---
    if query.data == BROWSE_PRODUCTS:
        await query.edit_message_text(text="Feature coming soon: Browse Products")
    elif query.data == VIEW_CART:
        await query.edit_message_text(text="Feature coming soon: View Cart")
    elif query.data == TRACK_ORDER:
        await query.edit_message_text(text="Feature coming soon: Track My Order")
    elif query.data == AI_ASSISTANT:
        await query.edit_message_text(text="Feature coming soon: AI Assistant")
    else:
        await query.edit_message_text(text="Unknown option selected.")


def setup_telegram_bot(application: Application) -> None:
    """Sets up the command and message handlers for the Telegram bot."""
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler)) # Handles all button clicks
    logger.info("Telegram bot handlers set up.")

