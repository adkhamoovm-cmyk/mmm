import re

with open("bot/handlers/admin.py", "r") as f:
    content = f.read()

if 'admin_promo_kb' not in content:
    content = content.replace(
        'from bot.keyboards import admin_main_kb, admin_cancel_kb, admin_user_kb, admin_settings_kb, main_menu_kb',
        'from bot.keyboards import admin_main_kb, admin_cancel_kb, admin_user_kb, admin_settings_kb, main_menu_kb, admin_promo_kb'
    )

    if 'UserPromo' not in content:
        content = content.replace('from bot.database import async_session, User, Transaction, Settings, PromoCode', 'from bot.database import async_session, User, Transaction, Settings, PromoCode, UserPromo')

    new_handlers = """
# --- PROMO CODES ---
@router.message(F.text == "🎁 Promokod yaratish")
async def admin_promo_main(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS: return
    await message.answer("🎁 Promokodlar boshqaruvi bo'limi", reply_markup=admin_promo_kb())
    await state.set_state(Admin.promo_menu)

@router.message(StateFilter(Admin.promo_menu), F.text == "➕ Yangi yaratish")
async def create_promo_start(message: Message, state: FSMContext):
    await message.answer("Yangi promokod uchun kod (nom) o'ylab toping:\nMasalan: BONUS5000", reply_markup=admin_cancel_kb())
    await state.set_state(Admin.waiting_for_promo_code)

@router.message(StateFilter(Admin.waiting_for_promo_code))
async def save_promo_code(message: Message, state: FSMContext):
    if message.text == "🔙 Admin menyu":
        await back_to_admin(message, state)
        return
        
    code = message.text.strip()
    
    async with async_session() as session:
        result = await session.execute(select(PromoCode).where(PromoCode.code == code))
        if result.scalars().first():
            await message.answer("Bunday kod allaqachon mavjud! Boshqa kod kiriting:")
            return
            
    await state.update_data(promo_code=code)
    await message.answer(f"Kod: {code}\nEndi ushbu kod uchun bitta odamga qancha miqdorda pul berilishini (UZS) kiriting:", reply_markup=admin_cancel_kb())
    await state.set_state(Admin.waiting_for_promo_amount)

@router.message(StateFilter(Admin.waiting_for_promo_amount))
async def save_promo_amount(message: Message, state: FSMContext):
    if message.text == "🔙 Admin menyu":
        await back_to_admin(message, state)
        return
        
    if not message.text.isdigit():
        await message.answer("Faqat raqam kiriting:")
        return
        
    amount = float(message.text)
    await state.update_data(promo_amount=amount)
    
    await message.answer(f"Summa: {amount:,.0f} UZS\nUshbu koddan umumiy hisobda necha kishi foydalana olishini kiriting (Limit):", reply_markup=admin_cancel_kb())
    await state.set_state(Admin.waiting_for_promo_limit)

@router.message(StateFilter(Admin.waiting_for_promo_limit))
async def save_promo_limit(message: Message, state: FSMContext):
    if message.text == "🔙 Admin menyu":
        await back_to_admin(message, state)
        return
        
    if not message.text.isdigit():
        await message.answer("Faqat raqam kiriting:")
        return
        
    limit = int(message.text)
    data = await state.get_data()
    code = data.get("promo_code")
    amount = data.get("promo_amount")
    
    async with async_session() as session:
        new_promo = PromoCode(code=code, amount=amount, limit=limit)
        session.add(new_promo)
        await session.commit()
        
    await message.answer(f"✅ Promokod muvaffaqiyatli yaratildi!\n\n🎁 Kod: {code}\n💰 Summa: {amount:,.0f} UZS\n👥 Limit: {limit} kishi", reply_markup=admin_promo_kb())
    await state.set_state(Admin.promo_menu)

@router.message(StateFilter(Admin.promo_menu), F.text == "📋 Promokodlar ro'yxati")
async def list_promos(message: Message, state: FSMContext):
    async with async_session() as session:
        result = await session.execute(select(PromoCode).order_by(PromoCode.id.desc()).limit(15))
        promos = result.scalars().all()
        
        if not promos:
            await message.answer("Hozircha promokodlar yo'q.", reply_markup=admin_promo_kb())
            return
            
        for promo in promos:
            text = f"🎁 Kod: <b>{promo.code}</b>\n💰 Summa: {promo.amount:,.0f} UZS\n" \
                   f"📊 Ishlatildi: {promo.used_count}/{promo.limit} kishi\n" \
                   f"🟢 Faol: {'Ha' if promo.is_active and promo.used_count < promo.limit else 'Yoq (Limit to\\'lgan yoki o\\'chirilgan)'}"
                   
            # Let's get the list of users who used it
            usage_res = await session.execute(select(UserPromo).where(UserPromo.promo_id == promo.id))
            usages = usage_res.scalars().all()
            if usages:
                text += "\\n\\n👥 Foydalanganlar:\\n"
                for u in usages:
                    user_data = await session.get(User, u.user_id)
                    if user_data:
                        text += f"👤 <a href='tg://user?id={user_data.id}'>{user_data.fullname}</a> (ID: {user_data.id})\\n"
                        
            await message.answer(text, parse_mode="HTML")
            
"""
    content += new_handlers

    with open("bot/handlers/admin.py", "w") as f:
        f.write(content)

