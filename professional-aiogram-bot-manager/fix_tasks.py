import re

with open("bot/handlers/tasks.py", "r") as f:
    content = f.read()

# Make sure we import timedelta
if 'timedelta' not in content:
    content = content.replace('from datetime import datetime', 'from datetime import datetime, timedelta')

new_logic_str = '''def get_task_date(dt: datetime):
    return (dt + timedelta(hours=5, minutes=-30)).date()

@router.message(F.text == "📦 BUYURTMALAR / VAZIFALAR")
async def tasks_menu(message: Message, state: FSMContext):
    now_utc = datetime.utcnow()
    current_task_date = get_task_date(now_utc)
    
    if current_task_date.weekday() == 6: # Sunday
        await message.answer("❌ Yakshanba — dam olish kuni. Pul yechish va vazifalar bajarish to'xtatilgan.", reply_markup=main_menu_kb())
        return'''

content = re.sub(
    r'@router\.message\(F\.text == "📦 BUYURTMALAR / VAZIFALAR"\)\nasync def tasks_menu\(message: Message, state: FSMContext\):\n\s+if datetime\.utcnow\(\)\.weekday\(\) == 6: # Sunday\n\s+await message\.answer\("❌ Yakshanba — dam olish kuni\. Pul yechish va vazifalar bajarish to\'xtatilgan\.", reply_markup=main_menu_kb\(\)\)\n\s+return',
    new_logic_str,
    content
)

content = content.replace('today = datetime.utcnow().date()', 'today = current_task_date')
content = content.replace('if shop.last_task_date and shop.last_task_date.date() < today:', 'if shop.last_task_date and get_task_date(shop.last_task_date) < today:')
content = content.replace('Yangi buyurtmalar ertaga soat 00:00 da yangilanadi.', 'Yangi buyurtmalar ertaga soat 00:30 da yangilanadi.')

with open("bot/handlers/tasks.py", "w") as f:
    f.write(content)
