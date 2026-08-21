import re

with open("bot/handlers/onboarding.py", "r") as f:
    content = f.read()

content = content.replace(
'''@router.message(F.text == "✅ Qoidalarga roziman")
async def tos_accept(message: Message, state: FSMContext):''',
'''@router.message(F.text == "✅ Qoidalarga roziman")
async def tos_accept(message: Message, state: FSMContext):
    async with async_session() as session:
        if await session.get(User, message.from_user.id):
            await message.answer("Asosiy menyu", reply_markup=main_menu_kb())
            return'''
)

content = content.replace(
'''        user = User(
            id=call.from_user.id,
            fullname=call.from_user.full_name,
            username=call.from_user.username,
            phone=phone,
            referrer_id=referrer_id
        )
        session.add(user)
        await session.commit()''',
'''        existing = await session.get(User, call.from_user.id)
        if existing:
            await call.message.delete()
            await call.message.answer("Siz allaqachon ro'yxatdan o'tgansiz.", reply_markup=main_menu_kb())
            await state.clear()
            return
            
        user = User(
            id=call.from_user.id,
            fullname=call.from_user.full_name,
            username=call.from_user.username,
            phone=phone,
            referrer_id=referrer_id
        )
        session.add(user)
        await session.commit()'''
)

with open("bot/handlers/onboarding.py", "w") as f:
    f.write(content)
