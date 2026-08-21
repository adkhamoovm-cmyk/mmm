import re

with open("bot/handlers/finance.py", "r") as f:
    content = f.read()

new_confirm = '''@router.callback_query(F.data == "with_confirm")
async def withdraw_confirm(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    amount = data.get("with_amount")
    final = data.get("with_final")
    
    if not amount or not final:
        await call.answer("❌ Xato: Ariza bekor qilingan yoki muddati o'tgan.", show_alert=True)
        await call.message.delete()
        return
        
    async with async_session() as session:
        user = await session.get(User, call.from_user.id)
        if user.balance < amount:
            await call.answer("Balans yetarli emas", show_alert=True)
            return
            
        user.balance -= amount'''

content = re.sub(
    r'@router\.callback_query\(F\.data == "with_confirm"\)\nasync def withdraw_confirm\(call: CallbackQuery, state: FSMContext\):\n    data = await state\.get_data\(\)\n    amount = data\.get\("with_amount"\)\n    final = data\.get\("with_final"\)\n\s+async with async_session\(\) as session:\n\s+user = await session\.get\(User, call\.from_user\.id\)\n\s+if user\.balance < amount:\n\s+await call\.answer\("Balans yetarli emas", show_alert=True\)\n\s+return\n\s+user\.balance -= amount',
    new_confirm,
    content
)

with open("bot/handlers/finance.py", "w") as f:
    f.write(content)

