with open("bot/handlers/cabinet.py", "r") as f:
    content = f.read()

if "from datetime import datetime" not in content:
    content = content.replace("from sqlalchemy import select, and_", "from sqlalchemy import select, and_\\nfrom datetime import datetime")

old_block = """        shop_text = "🏬 FAOL DO'KONLARINGIZ\\n"
        if not shops:
            shop_text += "Sizda faol do'konlar yo'q.\\n"
        else:
            for idx, shop in enumerate(shops, 1):
                rem_days = (shop.end_date - shop.start_date).days
                shop_name = {0: "Boshlang'ich Ombor", 1: "eBay Global", 2: "Walmart Direct", 3: "Amazon Prime"}.get(shop.tier, "Do'kon")
                shop_text += f"{idx}. {shop_name} — Qolgan muddat: {rem_days} kun\\n" """

new_block = """        shop_text = "🏬 FAOL DO'KONLARINGIZ\\n"
        active_count = 0
        for shop in shops:
            if shop.end_date < datetime.utcnow():
                shop.is_active = False
            else:
                active_count += 1
                rem_days = max(0, (shop.end_date - datetime.utcnow()).days)
                shop_name = {0: "Boshlang'ich Ombor", 1: "eBay Global", 2: "Walmart Direct", 3: "Amazon Prime"}.get(shop.tier, "Do'kon")
                shop_text += f"{active_count}. {shop_name} — Qolgan muddat: {rem_days} kun\\n"
        
        await session.commit()
                
        if active_count == 0:
            shop_text += "Sizda faol do'konlar yo'q.\\n" """

content = content.replace(old_block, new_block)

with open("bot/handlers/cabinet.py", "w") as f:
    f.write(content)
