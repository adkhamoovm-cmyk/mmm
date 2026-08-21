with open("bot/main.py", "r") as f:
    content = f.read()

replacement = """    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
"""
content = content.replace("    await bot.delete_webhook(drop_pending_updates=True)\n    await dp.start_polling(bot)", replacement)

with open("bot/main.py", "w") as f:
    f.write(content)
