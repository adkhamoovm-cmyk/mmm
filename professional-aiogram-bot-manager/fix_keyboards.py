import re

with open("bot/keyboards.py", "r") as f:
    content = f.read()

content = content.replace("KeyboardButton(text=\"🎁 Ombor balansni o'zgartirish\")", "KeyboardButton(text=\"🤝 Taklif qilganlar / Referallari\")")

with open("bot/keyboards.py", "w") as f:
    f.write(content)
