import asyncio
import time

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import BOT_TOKEN
from database import *
from mining import calculate_mining
from keyboards import main_menu

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):

    args = message.text.split()

    ref_by = 0

    if len(args) > 1:
        try:
            ref_by = int(args[1])
        except:
            pass

    await add_user(message.from_user.id, ref_by)

    user = await get_user(message.from_user.id)

    text = f"""
🚀 Welcome to Cloud Mining Bot

💰 Balance: {user[1]} TON
⚡ Speed: {user[2]} TON/sec

Use:
/mine - claim mining
/balance - check balance
/ref - referral link
"""

    await message.answer(
    text,
    reply_markup=main_menu
 )


@dp.message(lambda msg: msg.text == "💰 Balance")
async def balance_button(message: Message):

    user = await get_user(message.from_user.id)

    await message.answer(
        f"💰 Your balance: {user[1]} TON"
    )


@dp.message(lambda msg: msg.text == "⛏ Mine")
async def mine_button(message: Message):

    user = await get_user(message.from_user.id)

    balance = user[1]
    speed = user[2]
    last_claim = user[3]

    if last_claim == 0:
        last_claim = int(time.time())

    new_balance, now = calculate_mining(
        balance,
        speed,
        last_claim
    )

    await update_balance(
        message.from_user.id,
        new_balance
    )

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            "UPDATE users SET last_claim=? WHERE user_id=?",
            (now, message.from_user.id)
        )

        await db.commit()

    await message.answer(
        f"⛏ Mining claimed\n\n💰 Balance: {new_balance} TON"
    )


@dp.message(lambda msg: msg.text == "👥 Referral")
async def referral_button(message: Message):

    me = await bot.get_me()

    link = f"https://t.me/{me.username}?start={message.from_user.id}"

    await message.answer(
        f"👥 Your referral link:\n\n{link}"
    )


@dp.message(lambda msg: msg.text == "💎 Upgrade")
async def upgrade_button(message: Message):

    text = """
💎 Mining Plans

1 TON → Starter
5 TON → Pro
20 TON → Ultra

Send TON to:

UQXXXXXXXXXXXX

Then send transaction hash to admin.
"""

    await message.answer(text)


@dp.message(lambda msg: msg.text == "🏧 Withdraw")
async def withdraw_button(message: Message):

    await message.answer(
        "Send withdrawal like:\n\n/withdraw amount wallet"
    )


async def main():

    await init_db()

    print("Bot started...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
