import re

with open("bot/handlers/admin.py", "r") as f:
    content = f.read()

# Replace using regex to be safe
content = re.sub(r"else 'Yoq \(Limit to\\?'lgan\)'", 'else "Yoq (Limit tolgan)"', content)
content = content.replace("else 'Yoq (Limit to\\'lgan)'", 'else "Yoq (Limit tolgan)"')
content = content.replace("else 'Yoq (Limit to\\\\'lgan)'", 'else "Yoq (Limit tolgan)"')

with open("bot/handlers/admin.py", "w") as f:
    f.write(content)

