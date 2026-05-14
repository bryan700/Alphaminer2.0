from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⛏ Mine")],
        [
            KeyboardButton(text="💰 Balance"),
            KeyboardButton(text="👥 Referral")
        ],
        [
            KeyboardButton(text="💎 Upgrade"),
            KeyboardButton(text="🏧 Withdraw")
        ]
    ],
    resize_keyboard=True
)
