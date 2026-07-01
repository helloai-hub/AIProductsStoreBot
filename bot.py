import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

PRODUCTS = {
    "google": "🤖 Google AI Pro\n\n18 Months - 30,000 MMK\n12 Months - 25,000 MMK\n\n✅ Gemini AI Pro\n✅ Veo 3 Access\n✅ 5TB Storage\n⚡ Instant Activation\n❌ No Warranty",
    "grok": "🤖 Super Grok\n\n✅ 1 Month - 40,000 MMK\n✅ 3 Months - 80,000 MMK\n\n🛡 Full Warranty",
    "telegram": "💎 Telegram Premium\n\n💰 20,000 MMK\n🎁 CapCut Pro\n🔒 Individual / Private Account",
    "youtube": "🎥 YouTube Premium\n\n📈 Family Invite\n✅ Stable Service",
    "capcut": "🎁 CapCut Pro\n\n✅ Premium Features\n⚡ Fast Activation",
    "microsoft": "💼 Microsoft 365\n\n✅ Office Apps\n✅ OneDrive\n⚡ Instant Activation"
}

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Products", callback_data="products")],
        [InlineKeyboardButton("💳 Payment", callback_data="payment"),
         InlineKeyboardButton("📦 How to Order", callback_data="order")],
        [InlineKeyboardButton("💬 Contact Admin", url="https://t.me/Khuuzam")],
        [InlineKeyboardButton("❓ FAQ", callback_data="faq")]
    ])

def products_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 Google AI Pro", callback_data="google")],
        [InlineKeyboardButton("🤖 Super Grok", callback_data="grok")],
        [InlineKeyboardButton("💎 Telegram Premium", callback_data="telegram")],
        [InlineKeyboardButton("🎥 YouTube Premium", callback_data="youtube")],
        [InlineKeyboardButton("🎁 CapCut Pro", callback_data="capcut")],
        [InlineKeyboardButton("💼 Microsoft 365", callback_data="microsoft")],
        [InlineKeyboardButton("🔙 Back", callback_data="back")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🤖 Welcome to AI Products Store\n\nဘာလိုချင်ပါသလဲ?"
    await update.message.reply_text(text, reply_markup=main_menu())

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "products":
        await query.edit_message_text("🛒 Products List", reply_markup=products_menu())

    elif data in PRODUCTS:
        await query.edit_message_text(PRODUCTS[data], reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💳 Payment", callback_data="payment")],
            [InlineKeyboardButton("🔙 Back", callback_data="products")]
        ]))

    elif data == "payment":
        await query.edit_message_text(
            "💳 Payment Information\n\n"
            "🏦 KPay: 09 974 057 634\n"
            "📩 ငွေလွှဲပြီး Screenshot ကို ဒီ Bot ထဲပို့ပါ။\n"
            "Admin စစ်ပြီး အမြန်ဆုံးပြန်ဆက်သွယ်ပေးပါမယ်။",
            reply_markup=main_menu()
        )

    elif data == "order":
        await query.edit_message_text(
            "📦 How to Order\n\n"
            "1️⃣ Product ရွေးပါ\n"
            "2️⃣ Payment လွှဲပါ\n"
            "3️⃣ Screenshot ပို့ပါ\n"
            "4️⃣ Admin က စစ်ပြီး Activation လုပ်ပေးပါမယ်",
            reply_markup=main_menu()
        )

    elif data == "faq":
        await query.edit_message_text(
            "❓ FAQ\n\n"
            "Q: Admin မရှိရင်?\n"
            "A: Screenshot ပို့ထားခဲ့ပါ။ Online ဖြစ်တာနဲ့ ပြန်ဆက်သွယ်ပေးပါမယ်။\n\n"
            "Q: Warranty ရှိလား?\n"
            "A: Product အလိုက် မတူပါ။",
            reply_markup=main_menu()
        )

    elif data == "back":
        await query.edit_message_text("🤖 Welcome to AI Products Store\n\nဘာလိုချင်ပါသလဲ?", reply_markup=main_menu())

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text("✅ Screenshot လက်ခံရရှိပါပြီ။ Admin စစ်ပြီး ပြန်ဆက်သွယ်ပေးပါမယ်။")

    if ADMIN_ID:
        await context.bot.send_message(
            chat_id=int(ADMIN_ID),
            text=f"📸 New payment screenshot\n\nUser: @{user.username}\nName: {user.full_name}\nID: {user.id}"
        )
        await context.bot.forward_message(
            chat_id=int(ADMIN_ID),
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ 🤖 Menu ထဲက ခလုတ်တွေကိုရွေးပြီး အသုံးပြုနိုင်ပါတယ်။", reply_markup=main_menu())

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("products", start))
app.add_handler(CommandHandler("payment", start))
app.add_handler(CommandHandler("order", start))
app.add_handler(CommandHandler("contact", start))
app.add_handler(CommandHandler("faq", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

app.run_polling()
