import re

with open("bot/handlers/admin.py", "r") as f:
    content = f.read()

# Replace ombor balance with referrals
content = re.sub(
    r'@router\.message\(StateFilter\(Admin\.user_menu\), F\.text == "🎁 Ombor balansni o\'zgartirish"\)\nasync def (.*?)\n\s+await state\.set_state\(Admin\.waiting_for_ombor\)',
    '',
    content,
    flags=re.DOTALL
)

content = re.sub(
    r'@router\.message\(StateFilter\(Admin\.waiting_for_ombor\)\)\nasync def (.*?)await message\.answer\("Ombor balans saqlandi\.", reply_markup=admin_user_kb\(\)\)',
    '',
    content,
    flags=re.DOTALL
)

# Insert the referral logic handler
ref_handler = '''@router.message(StateFilter(Admin.user_menu), F.text == "🤝 Taklif qilganlar / Referallari")
async def admin_user_referrals(message: Message, state: FSMContext):
    data = await state.get_data()
    uid = data.get("admin_user_id")
    async with async_session() as session:
        user = await session.get(User, uid)
        text = f"👤 Foydalanuvchi: {user.fullname} (ID: {user.id})\\n\\n"
        if user.referrer_id:
            ref = await session.get(User, user.referrer_id)
            if ref:
                text += f"🔺 Uni taklif qilgan: <a href='tg://user?id={ref.id}'>{ref.fullname}</a> (ID: {ref.id})\\n\\n"
        else:
            text += "🔺 Uni hech kim taklif qilmagan.\\n\\n"
            
        result = await session.execute(select(User).where(User.referrer_id == uid))
        refs = result.scalars().all()
        text += f"🔻 U taklif qilgan a'zolar ({len(refs)} ta):\\n"
        for idx, r in enumerate(refs, 1):
            text += f"{idx}. <a href='tg://user?id={r.id}'>{r.fullname}</a> (ID: {r.id})\\n"
            
        await message.answer(text, reply_markup=admin_user_kb())
'''

# Find the end of the file or a good place to insert. We can just append it.
content += "\n" + ref_handler

with open("bot/handlers/admin.py", "w") as f:
    f.write(content)
