from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.ext import MessageHandler, filters

# ============================
# 🚀 START COMMAND → MAIN MENU
# ============================
from telegram import InlineKeyboardButton, InlineKeyboardMarkup  # Make sure you have these imported

async def start(update, context):
    user = update.effective_user.first_name
    chat_id = update.effective_chat.id

    # Send your image
    with open("welcome.jpg", "rb") as photo:
        await context.bot.send_photo(chat_id=chat_id, photo=photo)

    # Send welcome text and buttons
    keyboard = [
        [InlineKeyboardButton("Telugu Pack", callback_data="telugu_pack")],
        [InlineKeyboardButton("VIP Subscription", callback_data="vip_sub")],
        [InlineKeyboardButton("Movie Request", callback_data="movie_request")],
        [InlineKeyboardButton("Support / Contact", callback_data="support_contact")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"👋 Hi {user}! Welcome to the bot. Please choose an option:",
        reply_markup=reply_markup
    )

# ============================
# 📦 TELUGU PACK FLOW
# ============================
async def handle_telugu_pack(query):
    # Message you can change
    text = "📦 Telugu Pack selected.\nDo you want to buy this pack?"
    
    buttons = [
        [InlineKeyboardButton("✅ Yes", callback_data="telugu_yes"),
         InlineKeyboardButton("❌ No", callback_data="back_main")]
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))

# ============================
# 💎 VIP SUBSCRIPTION FLOW
# ============================
async def handle_vip_subscription(query):
    # Message you can change
    text = "💎 Choose your VIP plan:"
    
    buttons = [
        [InlineKeyboardButton("₹145 / 1 Month", callback_data="vip_1")],
        [InlineKeyboardButton("₹235 / 2 Months", callback_data="vip_2")],
        [InlineKeyboardButton("₹300 / 3 Months", callback_data="vip_3")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_main")]
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))

# ============================
# ✔️ CONFIRM VIP / TELUGU PACK
# ============================
async def ask_to_confirm_purchase(query, product_name):
    text = f"🛒 You selected: {product_name}\nDo you want to proceed?"
    buttons = [
        [InlineKeyboardButton("✅ Yes", callback_data=f"{product_name}_confirm"),
         InlineKeyboardButton("❌ No", callback_data="back_main")]
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))

# ============================
# 🤖 BUTTON HANDLER
# ============================
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "telugu_pack":
        await handle_telugu_pack(query)

    elif data == "telugu_yes":
        # 🔁 REPLACE this with your real message or forward logic
        await query.edit_message_text("📩 Sending Telugu Pack info...")

    elif data == "vip_sub":
        await handle_vip_subscription(query)

    elif data in ["vip_1", "vip_2", "vip_3"]:
        await ask_to_confirm_purchase(query, "VIP Subscription")

    elif data == "VIP Subscription_confirm":
        # 🔁 REPLACE this with your real message or forward logic
        await query.edit_message_text("✅ VIP Subscription confirmed. We will contact you!")

    elif data == "back_main":
        await start(update, context)

    else:
        await query.edit_message_text("⚠️ Unknown selection. Please use /start to begin again.")
        
async def handle_forwarded(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.full_name
    await update.message.reply_text(f"✅ Hi {user}, I got your forwarded message.")

# ============================
# ⚙️ BOT SETUP
# ============================
app = ApplicationBuilder().token("7903706087:AAFmT-iXEPtmQeccjxqYzyoMrN83oLe3i8o").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_buttons))
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_buttons))
app.add_handler(MessageHandler(filters.FORWARDED, handle_forwarded))

print("Bot is running...")
app.run_polling()
