import re

with open("bot/handlers/admin.py", "r") as f:
    content = f.read()

bad_line = """                   f"🟢 Faol: {'Ha' if promo.is_active and promo.used_count < promo.limit else "Yoq (Limit tolgan)"}\\n\\n\""""
replacement = """            faol_str = 'Ha' if promo.is_active and promo.used_count < promo.limit else 'Yoq (Limit tolgan)'
            text = f"🎁 Kod: <b>{promo.code}</b>\\n💰 Summa: {promo.amount:,.0f} UZS\\n" \\
                   f"📊 Ishlatildi: {promo.used_count}/{promo.limit} kishi\\n" \\
                   f"🟢 Faol: {faol_str}\\n\\n\""""

# Let's just do a string replacement for the text generation block
block_old = r"""            text = f"🎁 Kod: <b>{promo.code}</b>\n💰 Summa: {promo.amount:,.0f} UZS\n" \
                   f"📊 Ishlatildi: {promo.used_count}/{promo.limit} kishi\n" \
                   f"🟢 Faol: {'Ha' if promo.is_active and promo.used_count < promo.limit else "Yoq (Limit tolgan)"}\n\n\""""

block_new = r"""            faol_str = 'Ha' if promo.is_active and promo.used_count < promo.limit else 'Yoq (Limit)'
            text = f"🎁 Kod: <b>{promo.code}</b>\n💰 Summa: {promo.amount:,.0f} UZS\n" \
                   f"📊 Ishlatildi: {promo.used_count}/{promo.limit} kishi\n" \
                   f"🟢 Faol: {faol_str}\n\n" """

# Just use regex on the whole loop content
new_for_loop = """
        for promo in promos:
            faol_str = 'Ha' if promo.is_active and promo.used_count < promo.limit else 'Yoq (Limit to\\'lgan)'
            text = (f"🎁 Kod: <b>{promo.code}</b>\\n"
                   f"💰 Summa: {promo.amount:,.0f} UZS\\n"
                   f"📊 Ishlatildi: {promo.used_count}/{promo.limit} kishi\\n"
                   f"🟢 Faol: {faol_str}\\n\\n")
                   
            # Let's get the list of users who used it
            usage_res = await session.execute(select(UserPromo).where(UserPromo.promo_id == promo.id))
            usages = usage_res.scalars().all()
            if usages:
                text += "👥 Foydalanganlar:\\n"
                for u in usages:
                    user_data = await session.get(User, u.user_id)
                    if user_data:
                        text += f"👤 <a href='tg://user?id={user_data.id}'>{user_data.fullname}</a> (ID: {user_data.id})\\n"
                        
            await message.answer(text, parse_mode="HTML")
"""

start_idx = content.find('for promo in promos:')
clean_content = content[:start_idx]
# Wait, I need to make sure I don't delete other things, but this is at the end of the file.
with open("bot/handlers/admin.py", "w") as f:
    f.write(clean_content + new_for_loop)
