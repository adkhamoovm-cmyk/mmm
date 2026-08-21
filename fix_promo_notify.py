import re

with open("bot/handlers/promo.py", "r") as f:
    content = f.read()

if 'ADMIN_IDS' not in content:
    content = content.replace('from bot.keyboards import main_menu_kb, back_kb', 'from bot.keyboards import main_menu_kb, back_kb\nfrom bot.config import ADMIN_IDS')
    
    notify_logic = """
        await msg.delete()
        await message.answer(f"🎉 Tabriklaymiz! Sirli xalta ochildi! Kodingiz muvaffaqiyatli qabul qilindi. Balansingiz +{promo.amount:,.0f} UZS ga ko'paydi!", reply_markup=main_menu_kb())
        await state.clear()
        
        # Adminlarga xabar yuborish
        for admin_id in ADMIN_IDS:
            try:
                await message.bot.send_message(
                    admin_id, 
                    f"🎁 <b>Yangi promokoddan foydalanish!</b>\\n\\n"
                    f"👤 Mijoz: <a href='tg://user?id={user.id}'>{user.fullname}</a> (ID: {user.id})\\n"
                    f"🎟 Promokod: <b>{promo.code}</b>\\n"
                    f"💰 Olingan summa: {promo.amount:,.0f} UZS\\n"
                    f"📊 Limit holati: {promo.used_count}/{promo.limit}",
                    parse_mode="HTML"
                )
            except:
                pass
"""
    content = content.replace(
"""        await msg.delete()
        await message.answer(f"🎉 Tabriklaymiz! Sirli xalta ochildi! Kodingiz muvaffaqiyatli qabul qilindi. Balansingiz +{promo.amount:,.0f} UZS ga ko'paydi!", reply_markup=main_menu_kb())
        await state.clear()""", notify_logic)

    with open("bot/handlers/promo.py", "w") as f:
        f.write(content)

