from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message
from bot.keyboards import shops_kb, main_menu_kb, cabinet_kb
from bot.database import async_session, User, PromoCode, UserPromo, Transaction
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(F.text == "⬅️ Asosiy menyu")
async def back_to_main(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Asosiy menyuga qaytdingiz.", reply_markup=main_menu_kb())

@router.message(F.text == "🏢 Biz haqimizda")
async def about_us_menu(message: Message):
    text = "🏢 <b>E-Tycoon — Xalqaro Elektron Tijorat Simulyatori</b>\n\n" \
           "Bizning platforma orqali siz yirik xalqaro marketplacelarda (eBay, Walmart, Amazon) o'z virtual do'koningizni ochishingiz va " \
           "elektron tijorat jarayonlarini (buyurtmalarni qadoqlash, kuryerga topshirish, mijozlar bahosi) simulyatsiya qilish orqali " \
           "real daromad topishingiz mumkin.\n\n" \
           "🌟 <b>Nima uchun bizni tanlashadi?</b>\n" \
           "• Qulay va interaktiv interfeys\n" \
           "• Tezkor to'lovlar va shaffof moliya tizimi\n" \
           "• Do'stlarni taklif qilib, qo'shimcha passiv daromad topish imkoniyati\n\n" \
           "Biz bilan o'z biznesingizni boshlang va muvaffaqiyatga erishing! 🚀"
    await message.answer(text, reply_markup=main_menu_kb())

@router.message(F.text == "ℹ️ Yordam / FAQ")
async def faq_menu(message: Message):
    text = "ℹ️ <b>KO'P BERILADIGAN SAVOLLAR (FAQ)</b>\n\n" \
           "🔹 <b>1. E-Tycoon platformasi nima?</b>\n" \
           "Bu xalqaro marketplace do'konlarini boshqarishga asoslangan virtual elektron tijorat simulyatoridir.\n\n" \
           "🔹 <b>2. Boshlang'ich Ombordan kelgan pulni yechsa bo'ladimi?</b>\n" \
           "Yo'q, Ombor foydasi faqat pullik do'konlarni xarid qilishda chegirma (bonus) sifatida ishlatiladi.\n\n" \
           "🔹 <b>3. Qachon pul yechishim mumkin?</b>\n" \
           "Kamida bitta pullik do'kon xarid qilganingizdan so'ng, Dushanba-Shanba kunlari soat 10:00 dan 17:00 gacha.\n\n" \
           "🔹 <b>4. Nega Yakshanba dam olish kuni?</b>\n" \
           "Yakshanba moliya bo'limi va tizim texnik xizmati uchun rasmiy dam olish kuni hisoblanadi.\n\n" \
           "🔹 <b>5. Pul yechishda komissiya qancha?</b>\n" \
           "Tizim orqali pul yechishda 11% xizmat haqi ushlab qolinadi.\n\n" \
           "🔹 <b>6. Nechta do'kon ochish mumkin?</b>\n" \
           "Bir foydalanuvchida maksimal 3 ta faol do'kon bo'lishi mumkin. Ularning muddati 60 kundan iborat.\n\n" \
           "🔹 <b>7. Referal daromadi qachon tushadi?</b>\n" \
           "Taklif qilgan do'stingiz yangi do'kon ijaraga olgan zahoti uning xarididan foiz asosiy balansingizga tushadi.\n\n" \
           "👨‍💻 <b>Yordam uchun:</b> @ETycoon_Support"
    await message.answer(text, reply_markup=main_menu_kb())

@router.message(F.text == "🌐 Hamkorlik")
async def referral_menu(message: Message):
    async with async_session() as session:
        user = await session.get(User, message.from_user.id)
        if not user:
            return
            
    link = f"https://t.me/E_TycoonBot?start=ref_{user.id}"
    text = f"🌐 HAMKORLIK DASTURI (REFERAL)\n\n" \
           f"🔗 Sizning shaxsiy referal havolangiz: {link}\n\n" \
           f"📊 SIZNING UMUMIY STATISTIKANGIZ\n" \
           f"💰 Jami referal daromadi: {user.ref_profit_total:,.0f} UZS\n\n" \
           f"⚠️ FOIZLAR VA TAKRORIY XARID QOIDASI:\n" \
           f"• A-daraja: Yangi tarif xaridi uchun 7% (Takroriy 4%).\n" \
           f"• B-daraja: Yangi tarif xaridi uchun 3% (Takroriy 1.5%).\n" \
           f"• C-daraja: Barcha xaridlar uchun doimiy 0.5%.\n"
           
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    share_url = f"https://t.me/share/url?url={link}&text=Ajoyib%20e-tijorat%20simulyatori!%20Shu%20havola%20orqali%20ro'yxatdan%20o'ting"
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="↗️ Havolani do'stlarga yuborish", url=share_url)]])
    
    await message.answer(text, reply_markup=kb, disable_web_page_preview=True)
