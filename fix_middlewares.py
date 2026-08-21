import re

with open("bot/middlewares.py", "r") as f:
    content = f.read()

new_logic = '''            if user and user.is_banned:
                if isinstance(event, Message):
                    await event.answer("🚫 Kechirasiz, sizning akkauntingiz bloklangan.")
                elif isinstance(event, CallbackQuery):
                    await event.answer("🚫 Akkauntingiz bloklangan.", show_alert=True)
                return
                
            # Restrict unregistered users
            is_start_cmd = isinstance(event, Message) and event.text and event.text.startswith("/start")
            is_tos = isinstance(event, Message) and event.text == "✅ Qoidalarga roziman"
            is_contact = isinstance(event, Message) and event.contact is not None
            is_check_sub = isinstance(event, CallbackQuery) and event.data == "check_sub"
            
            if not user and not (is_start_cmd or is_tos or is_contact or is_check_sub):
                if isinstance(event, Message):
                    await event.answer("Siz ro'yxatdan o'tmagansiz. Qaytadan boshlash uchun /start ni bosing.")
                elif isinstance(event, CallbackQuery):
                    await event.answer("Ro'yxatdan o'tmagansiz.", show_alert=True)
                return'''

content = content.replace('''            if user and user.is_banned:
                if isinstance(event, Message):
                    await event.answer("🚫 Kechirasiz, sizning akkauntingiz bloklangan.")
                elif isinstance(event, CallbackQuery):
                    await event.answer("🚫 Akkauntingiz bloklangan.", show_alert=True)
                return''', new_logic)

with open("bot/middlewares.py", "w") as f:
    f.write(content)
