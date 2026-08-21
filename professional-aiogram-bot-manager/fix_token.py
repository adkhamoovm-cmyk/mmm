with open("bot/config.py", "r") as f:
    content = f.read()

content = content.replace("8969356827:AAFxYaU-hmSUiTfK6y12MJsnmHZh5szI_PQ", "8969356827:AAF5hb41JUta2kuQOzd5LbEPxMp7aCKmATU")

with open("bot/config.py", "w") as f:
    f.write(content)
