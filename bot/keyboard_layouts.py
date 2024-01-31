from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Define keyboards
MAIN_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔍 Run search", callback_data='run_search')],
    [InlineKeyboardButton("ℹ️ Get Info", callback_data='get_info')]
])

RETURN_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("◀️ Return", callback_data='return')]
])

SEARCH_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔍 Quick search", callback_data='quick_search'),
     InlineKeyboardButton("🕵️ Deep search", callback_data='deep_search')],
    [InlineKeyboardButton("◀️ Return", callback_data='return')]
])

