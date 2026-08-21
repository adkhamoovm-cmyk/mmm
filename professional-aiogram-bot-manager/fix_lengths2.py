import re

with open("bot/handlers/cabinet.py", "r") as f:
    content = f.read()

content = content.replace(
'''    await state.update_data(card_name=message.text)
    await message.answer("Karta turini tanlang:", reply_markup=card_type_kb())''',
'''    if len(message.text) > 60:
        await message.answer("Ism juda uzun, qisqaroq kiriting:")
        return
    await state.update_data(card_name=message.text)
    await message.answer("Karta turini tanlang:", reply_markup=card_type_kb())'''
)

with open("bot/handlers/cabinet.py", "w") as f:
    f.write(content)
