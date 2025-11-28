import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

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

# Menu categories (sample for Phase 1 UI)
CATEGORIES = [
    "Skin Care",
    "Hair Care",
    "Makeup",
    "Perfume",
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a minimal welcome message."""
    user = update.effective_user
    logger.info("/start invoked by user=%s id=%s", user.username, user.id)

    keyboard = [
        [InlineKeyboardButton("1️⃣ Browse Products", callback_data=BROWSE_PRODUCTS)],
        [InlineKeyboardButton("2️⃣ View Cart", callback_data=VIEW_CART)],
        [InlineKeyboardButton("3️⃣ Track Order", callback_data=TRACK_ORDER)],
        [InlineKeyboardButton("4️⃣ AI Assistant", callback_data=AI_ASSISTANT)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_html(
        f"🌸 Welcome, {user.mention_html()}!\nChoose an option below:", reply_markup=reply_markup
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    logger.info("callback received from user=%s id=%s data=%s", user.username, user.id, query.data)

    # Top-level menu actions for Phase 1
    if query.data == BROWSE_PRODUCTS:
        # show sample categories as buttons
        keyboard = [[InlineKeyboardButton(cat, callback_data=f"category:{cat}")] for cat in CATEGORIES]
        keyboard.append([InlineKeyboardButton("Back", callback_data="back_to_menu")])
        await query.edit_message_text(text="Select a category:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data and query.data.startswith("category:"):
        # For phase 1 we show a placeholder list; real product list will come in Phase 2
        category = query.data.split(":", 1)[1]
        await query.edit_message_text(text=f"Products for category: {category}\nFeature coming soon: real product list.")

    elif query.data == VIEW_CART:
        await query.edit_message_text(text="Feature coming soon: View Cart")

    elif query.data == TRACK_ORDER:
        await query.edit_message_text(text="To track an order, send /track <order_id> in this chat.")

    elif query.data == AI_ASSISTANT:
        await query.edit_message_text(text="AI Assistant is coming soon — stay tuned!")

    elif query.data == "back_to_menu":
        # Recreate the main menu
        await start(update, context)

    else:
        await query.edit_message_text(text="Unknown option selected.")


async def track_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    args = context.args
    logger.info("/track invoked by user=%s id=%s args=%s", user.username, user.id, args)
    if not args:
        await update.message.reply_text("Usage: /track <order_id> — provide an order id to track.")
        return
    order_id = args[0]
    # Phase 1: stubbed response
    await update.message.reply_text(f"Tracking for order {order_id}: feature coming soon (stub).")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    logger.info("/help invoked by user=%s id=%s", user.username, user.id)
    await update.message.reply_text("Available commands:\n/start - Open main menu\n/track <order_id> - Track an order")


def create_application(token: str) -> Application:
    """Build and return a telegram Application with minimal handlers.

    The function does not start the application; it only configures handlers.
    Caller is responsible for running `application.run_polling()`.
    """
    application = Application.builder().token(token).build()
    # Phase 1 handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("track", track_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    logger.info("Telegram bot application created (handlers registered).")
    return application



