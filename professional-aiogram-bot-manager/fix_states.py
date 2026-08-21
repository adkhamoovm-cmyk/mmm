import os
import re

for file in os.listdir('bot/handlers'):
    if not file.endswith('.py'): continue
    path = f'bot/handlers/{file}'
    with open(path, 'r') as f:
        content = f.read()
    
    # Add StateFilter import if not there
    if 'from aiogram.filters import StateFilter' not in content:
        content = content.replace('from aiogram.filters import Command', 'from aiogram.filters import Command, StateFilter')
        if 'StateFilter' not in content:
            content = content.replace('from aiogram import Router, F', 'from aiogram import Router, F\nfrom aiogram.filters import StateFilter')
            
    content = re.sub(r'@router\.message\(([A-Z][a-zA-Z0-9_]*\.[a-zA-Z0-9_]+)\)', r'@router.message(StateFilter(\1))', content)
    content = re.sub(r'@router\.message\(([A-Z][a-zA-Z0-9_]*\.[a-zA-Z0-9_]+), F\.', r'@router.message(StateFilter(\1), F.', content)
    
    with open(path, 'w') as f:
        f.write(content)
