from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Create a custom keyboard
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🎵 Recognize Song")], [KeyboardButton(text="ℹ️ Help")]],
    resize_keyboard=True,  # Resize the keyboard to fit the buttons
    one_time_keyboard=True,  # Hide the keyboard after a button is pressed
)
