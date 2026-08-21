import re

with open("bot/handlers/admin.py", "r") as f:
    content = f.read()

content = content.replace("else 'Yoq (Limit to\\'lgan)'", 'else "Yoq (Limit to\'lgan)"')

with open("bot/handlers/admin.py", "w") as f:
    f.write(content)

