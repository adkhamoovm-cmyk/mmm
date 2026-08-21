import re

with open("bot/handlers/shops.py", "r") as f:
    content = f.read()

content = content.replace(
'''        # Deduct balance
        total_balance = user.balance + user.ombor_balance
        if total_balance < price:
            await message.answer(f"❌ Mablag' yetishmovchiligi. Do'kon narxi {price:,.0f} UZS. Hisobingizni to'ldiring.", reply_markup=main_menu_kb())
            return
        
        # Deduct from ombor first, then main balance
        rem_price = price
        if user.ombor_balance >= rem_price:
            user.ombor_balance -= rem_price
            rem_price = 0
        else:
            rem_price -= user.ombor_balance
            user.ombor_balance = 0
            
        user.balance -= rem_price''',
'''        # Deduct balance
        if user.balance < price:
            await message.answer(f"❌ Mablag' yetishmovchiligi. Do'kon narxi {price:,.0f} UZS. Hisobingizni to'ldiring.", reply_markup=main_menu_kb())
            return
            
        user.balance -= price'''
)

content = content.replace("await process_referral_bonus(user_id, price, tier, session)", "await process_referral_bonus(user, price, tier, session, message.bot, shop_info['name'])")

old_bonus_logic = '''async def process_referral_bonus(user_id: int, price: float, tier: int, session):
    if price <= 0:
        return
        
    user = await session.get(User, user_id)
    if not user.referrer_id:
        return
        
    # Check if returning (downgrade logic)
    result = await session.execute(select(Shop).where(and_(Shop.user_id == user_id, Shop.tier == tier)))
    is_returning = len(result.scalars().all()) > 1
    
    percents = {
        'A': 4.0 if is_returning else 7.0,
        'B': 1.5 if is_returning else 3.0,
        'C': 0.5
    }
    
    # Process A
    ref_a = await session.get(User, user.referrer_id)
    if ref_a:
        bonus_a = (price * percents['A']) / 100
        ref_a.balance += bonus_a
        ref_a.ref_profit_total += bonus_a
        session.add(Transaction(user_id=ref_a.id, type="ref_bonus", amount=bonus_a, status="completed"))
        
        # Process B
        if ref_a.referrer_id:
            ref_b = await session.get(User, ref_a.referrer_id)
            if ref_b:
                bonus_b = (price * percents['B']) / 100
                ref_b.balance += bonus_b
                ref_b.ref_profit_total += bonus_b
                session.add(Transaction(user_id=ref_b.id, type="ref_bonus", amount=bonus_b, status="completed"))
                
                # Process C
                if ref_b.referrer_id:
                    ref_c = await session.get(User, ref_b.referrer_id)
                    if ref_c:
                        bonus_c = (price * percents['C']) / 100
                        ref_c.balance += bonus_c
                        ref_c.ref_profit_total += bonus_c
                        session.add(Transaction(user_id=ref_c.id, type="ref_bonus", amount=bonus_c, status="completed"))
                        
    await session.commit()'''

new_bonus_logic = '''async def process_referral_bonus(user: User, price: float, tier: int, session, bot, shop_name: str):
    if price <= 0:
        return
        
    if not user.referrer_id:
        return
        
    user_link = f"<a href='tg://user?id={user.id}'>{user.fullname}</a>"
    if user.username:
        user_link = f"<a href='tg://user?id={user.id}'>@{user.username}</a>"
        
    # Check if returning (downgrade logic)
    result = await session.execute(select(Shop).where(and_(Shop.user_id == user.id, Shop.tier == tier)))
    is_returning = len(result.scalars().all()) > 1
    
    percents = {
        'A': 4.0 if is_returning else 7.0,
        'B': 1.5 if is_returning else 3.0,
        'C': 0.5
    }
    
    # Process A
    ref_a = await session.get(User, user.referrer_id)
    if ref_a:
        bonus_a = (price * percents['A']) / 100
        ref_a.balance += bonus_a
        ref_a.ref_profit_total += bonus_a
        session.add(Transaction(user_id=ref_a.id, type="ref_bonus", amount=bonus_a, status="completed"))
        try:
            await bot.send_message(ref_a.id, f"🎉 Sizning A-darajali a'zoingiz {user_link} <b>{shop_name}</b> do'konini xarid qildi!\\nSiz {bonus_a:,.0f} UZS daromadga ega bo'ldingiz. Ishonch uchun rahmat!")
        except Exception:
            pass
        
        # Process B
        if ref_a.referrer_id:
            ref_b = await session.get(User, ref_a.referrer_id)
            if ref_b:
                bonus_b = (price * percents['B']) / 100
                ref_b.balance += bonus_b
                ref_b.ref_profit_total += bonus_b
                session.add(Transaction(user_id=ref_b.id, type="ref_bonus", amount=bonus_b, status="completed"))
                try:
                    await bot.send_message(ref_b.id, f"🎉 Sizning B-darajali a'zoingiz {user_link} <b>{shop_name}</b> do'konini xarid qildi!\\nSiz {bonus_b:,.0f} UZS daromadga ega bo'ldingiz. Ishonch uchun rahmat!")
                except Exception:
                    pass
                
                # Process C
                if ref_b.referrer_id:
                    ref_c = await session.get(User, ref_b.referrer_id)
                    if ref_c:
                        bonus_c = (price * percents['C']) / 100
                        ref_c.balance += bonus_c
                        ref_c.ref_profit_total += bonus_c
                        session.add(Transaction(user_id=ref_c.id, type="ref_bonus", amount=bonus_c, status="completed"))
                        try:
                            await bot.send_message(ref_c.id, f"🎉 Sizning C-darajali a'zoingiz {user_link} <b>{shop_name}</b> do'konini xarid qildi!\\nSiz {bonus_c:,.0f} UZS daromadga ega bo'ldingiz. Ishonch uchun rahmat!")
                        except Exception:
                            pass
                        
    await session.commit()'''

content = content.replace(old_bonus_logic, new_bonus_logic)

with open("bot/handlers/shops.py", "w") as f:
    f.write(content)

