with open("bot/handlers/cabinet.py", "r") as f:
    content = f.read()

content = content.replace("from sqlalchemy import select, and_\\nfrom datetime import datetime", "from sqlalchemy import select, and_\nfrom datetime import datetime")

with open("bot/handlers/cabinet.py", "w") as f:
    f.write(content)

