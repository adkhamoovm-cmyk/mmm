import re

with open("bot/handlers/finance.py", "r") as f:
    content = f.read()

content = content.replace(
'''    if not message.text.isdigit():
        await message.answer("Faqat raqam kiriting.")
        return
        
    amount = int(message.text)''',
'''    if not message.text.isdigit():
        await message.answer("Faqat raqam kiriting.")
        return
        
    if len(message.text) > 15:
        await message.answer("Summa juda katta.")
        return
        
    amount = int(message.text)'''
)

content = content.replace(
'''    if not message.text.isdigit():
        return
        
    amount = int(message.text)''',
'''    if not message.text.isdigit():
        return
        
    if len(message.text) > 15:
        await message.answer("Summa juda katta.")
        return
        
    amount = int(message.text)'''
)

with open("bot/handlers/finance.py", "w") as f:
    f.write(content)
