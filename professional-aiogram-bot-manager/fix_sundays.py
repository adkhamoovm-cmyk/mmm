with open("bot/handlers/shops.py", "r") as f:
    content = f.read()

replacement = """
def add_working_days(start_date, working_days):
    current = start_date
    added = 0
    while added < working_days:
        current += timedelta(days=1)
        if current.weekday() != 6: # 6 is Sunday
            added += 1
    return current

@router.callback_query(F.data.startswith("buy_shop_"))
async def process_buy_shop(call: CallbackQuery):
"""

content = content.replace('@router.callback_query(F.data.startswith("buy_shop_"))\nasync def process_buy_shop(call: CallbackQuery):', replacement)

old_logic = 'end_date = datetime.utcnow() + timedelta(days=shop_info["days"])'
new_logic = 'end_date = add_working_days(datetime.utcnow(), shop_info["days"])'

content = content.replace(old_logic, new_logic)

with open("bot/handlers/shops.py", "w") as f:
    f.write(content)
