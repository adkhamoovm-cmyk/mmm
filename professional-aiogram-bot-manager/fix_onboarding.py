import re

with open("bot/handlers/onboarding.py", "r") as f:
    content = f.read()

new_logic = '''        session.add(user)
        await session.commit()
        
        if referrer_id:
            try:
                user_link = f"<a href='tg://user?id={call.from_user.id}'>{call.from_user.full_name}</a>"
                if call.from_user.username:
                    user_link = f"<a href='tg://user?id={call.from_user.id}'>@{call.from_user.username}</a>"
                await bot.send_message(
                    referrer_id, 
                    f"🎉 <b>Yangi a'zo qo'shildi!</b>\\n\\nSizda yangi a'zo ro'yxatdan o'tdi: {user_link}\\nUnga yo'l ko'rsating, birgalikda E-Tycoon bilan daromad toping!"
                )
            except Exception:
                pass'''

content = content.replace("        session.add(user)\n        await session.commit()", new_logic)

with open("bot/handlers/onboarding.py", "w") as f:
    f.write(content)
