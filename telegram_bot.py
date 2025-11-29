import logging
import os
import httpx
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
        # For Phase 2: fetch products from DB via services if available
        category = query.data.split(":", 1)[1]
        services = context.application.bot_data.get("services")
        db = context.application.bot_data.get("db")
        if services is None:
            await query.edit_message_text(text=f"Products for category: {category}\nDB not available yet.")
            return

        try:
            products = await services.get_products(db, limit=5, skip=0, filters={"category": category})
        except Exception:
            products = []

        if not products:
            await query.edit_message_text(text=f"No products found for category: {category}")
            return

        # Build a keyboard of product buttons
        keyboard = [[InlineKeyboardButton(p.get("name") or "Unnamed", callback_data=f"product:{p.get('id')}")] for p in products]
        keyboard.append([InlineKeyboardButton("Back", callback_data="back_to_menu")])
        await query.edit_message_text(text=f"Products for category: {category}", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == VIEW_CART:
        await query.edit_message_text(text="Feature coming soon: View Cart")

    elif query.data == TRACK_ORDER:
        await query.edit_message_text(text="To track an order, send /track <order_id> in this chat.")

    elif query.data == AI_ASSISTANT:
        await query.edit_message_text(text="AI Assistant is coming soon — stay tuned!")

    elif query.data and query.data.startswith("product:"):
        product_id = query.data.split(":", 1)[1]
        services = context.application.bot_data.get("services")
        db = context.application.bot_data.get("db")
        if services is None:
            await query.edit_message_text(text="Product details unavailable: DB not connected.")
            return
        product = await services.get_product_by_id(db, product_id)
        if not product:
            await query.edit_message_text(text="Product not found.")
            return

        # Build product detail text (Name, Price, Description, Rating)
        name = product.get("name") or "Unnamed"
        price = product.get("price")
        currency = product.get("currency") or ""
        desc = product.get("description") or "No description available."
        # rating may be present on the product doc (0-5). If absent, show 'No rating'.
        rating_value = product.get("rating")
        if rating_value is None:
            rating_text = "No rating"
        else:
            try:
                r = float(rating_value)
                filled = int(round(r))
                stars = '⭐' * max(0, min(5, filled))
                empty = '☆' * (5 - max(0, min(5, filled)))
                rating_text = f"{stars}{empty} ({r:.1f})"
            except Exception:
                rating_text = str(rating_value)

        # Format message using HTML for bold name
        text = f"<b>{name}</b>\nPrice: {price} {currency}\n\n{desc}\n\n⭐ Rating: {rating_text}"

        # Detail buttons (Add to cart/wishlist/back)
        kb = [
            [InlineKeyboardButton("Add to Cart", callback_data=f"cart:add:{product_id}"), InlineKeyboardButton("Add to Wishlist", callback_data=f"wish:add:{product_id}" )],
            [InlineKeyboardButton("Back", callback_data="back_to_menu")],
        ]

        # If there is an image we can send it as a photo with caption; otherwise edit message text
        images = product.get("images") or []
        if images:
            # send photo and replace the current message
            try:
                await query.message.reply_photo(photo=images[0], caption=text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='HTML')
                await query.delete_message()
            except Exception:
                await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='HTML')
        else:
            await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='HTML')

    elif query.data and query.data.startswith("cart:add:"):
        # Add product to user's cart via backend telegram endpoint
        product_id = query.data.split(":", 2)[2]
        backend = os.getenv("BACKEND_URL") or "http://localhost:5000"
        telegram_id = str(user.id)
        payload = {"telegram_id": telegram_id, "product_id": product_id, "quantity": 1}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(f"{backend}/api/telegram/cart/add", json=payload)
            if resp.status_code >= 200 and resp.status_code < 300:
                await query.answer(text="Added to cart", show_alert=False)
                # Optionally update the message to show a confirmation
                await query.message.reply_text("✅ Product added to your cart.")
            else:
                await query.answer(text="Failed to add to cart", show_alert=True)
                await query.message.reply_text(f"Failed to add to cart: {resp.status_code} {resp.text}")
        except Exception as e:
            logger.exception("Error calling backend cart add: %s", e)
            await query.answer(text="Error adding to cart", show_alert=True)
            await query.message.reply_text("An error occurred while adding to cart.")

    elif query.data and query.data.startswith("wish:add:"):
        # Wishlist fallback: call the cart add endpoint with an as_wishlist flag.
        product_id = query.data.split(":", 2)[2]
        backend = os.getenv("BACKEND_URL") or "http://localhost:5000"
        telegram_id = str(user.id)
        payload = {"telegram_id": telegram_id, "product_id": product_id, "quantity": 1, "as_wishlist": True}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(f"{backend}/api/telegram/cart/add", json=payload)
            if resp.status_code >= 200 and resp.status_code < 300:
                await query.answer(text="Added to wishlist (saved)", show_alert=False)
                await query.message.reply_text("💖 Product saved (wishlist fallback).")
            else:
                await query.answer(text="Failed to save to wishlist", show_alert=True)
                await query.message.reply_text(f"Failed to save to wishlist: {resp.status_code} {resp.text}")
        except Exception as e:
            logger.exception("Error calling backend wishlist add: %s", e)
            await query.answer(text="Error saving to wishlist", show_alert=True)
            await query.message.reply_text("An error occurred while saving to wishlist.")

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



