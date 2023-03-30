from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOPICS_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
COMPLEXITY_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
GREETING = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

# BUTTON_MATH = KeyboardButton('математика')
# BUTTON_STRINGS = KeyboardButton('Строки')
# BUTTON_800 = KeyboardButton('900')
# TOPICS_KEYBOARD.add(BUTTON_MATH)
# COMPLEXITY_KEYBOARD.add(BUTTON_800)
GREETING.add(KeyboardButton("Подобрать задачи"))
