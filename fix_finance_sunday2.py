import re

with open("bot/handlers/finance.py", "r") as f:
    content = f.read()

# Make sure we import timedelta
if 'timedelta' not in content:
    content = content.replace('from datetime import datetime', 'from datetime import datetime, timedelta')

content = content.replace(
'''    if datetime.utcnow().weekday() == 6:
        await message.answer("❌ Yakshanba kuni pul yechib bo'lmaydi.")
        return
        
    hour = datetime.utcnow().hour + 5 # Uzb time approx''',
'''    uzb_time = datetime.utcnow() + timedelta(hours=5)
    if uzb_time.weekday() == 6:
        await message.answer("❌ Yakshanba kuni pul yechib bo'lmaydi.")
        return
        
    hour = uzb_time.hour'''
)

with open("bot/handlers/finance.py", "w") as f:
    f.write(content)
