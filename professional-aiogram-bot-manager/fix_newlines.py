import re

with open("bot/handlers/admin.py", "r") as f:
    content = f.read()

content = content.replace("Yangi promokod uchun kod (nom) o'ylab toping:\nMasalan: BONUS5000\"", "Yangi promokod uchun kod (nom) o'ylab toping:\\nMasalan: BONUS5000\"")
content = content.replace(f'await message.answer(f"Kod: {{code}}\nEndi ushbu kod uchun bitta odamga qancha miqdorda pul berilishini (UZS) kiriting:", reply_markup=admin_cancel_kb())', f'await message.answer(f"Kod: {{code}}\\nEndi ushbu kod uchun bitta odamga qancha miqdorda pul berilishini (UZS) kiriting:", reply_markup=admin_cancel_kb())')
content = content.replace(f'await message.answer(f"Summa: {{amount:,.0f}} UZS\nUshbu koddan umumiy hisobda necha kishi foydalana olishini kiriting (Limit):", reply_markup=admin_cancel_kb())', f'await message.answer(f"Summa: {{amount:,.0f}} UZS\\nUshbu koddan umumiy hisobda necha kishi foydalana olishini kiriting (Limit):", reply_markup=admin_cancel_kb())')
content = content.replace(f'await message.answer(f"✅ Promokod muvaffaqiyatli yaratildi!\n\n🎁 Kod: {{code}}\n💰 Summa: {{amount:,.0f}} UZS\n👥 Limit: {{limit}} kishi", reply_markup=admin_promo_kb())', f'await message.answer(f"✅ Promokod muvaffaqiyatli yaratildi!\\n\\n🎁 Kod: {{code}}\\n💰 Summa: {{amount:,.0f}} UZS\\n👥 Limit: {{limit}} kishi", reply_markup=admin_promo_kb())')
content = content.replace(f'text = f"🎁 Kod: <b>{{promo.code}}</b>\n💰 Summa: {{promo.amount:,.0f}} UZS\n" \\', f'text = f"🎁 Kod: <b>{{promo.code}}</b>\\n💰 Summa: {{promo.amount:,.0f}} UZS\\n" \\')
content = content.replace(f'f"📊 Ishlatildi: {{promo.used_count}}/{{promo.limit}} kishi\n" \\', f'f"📊 Ishlatildi: {{promo.used_count}}/{{promo.limit}} kishi\\n" \\')


with open("bot/handlers/admin.py", "w") as f:
    f.write(content)

