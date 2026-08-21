FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set python path and run the bot
ENV PYTHONPATH=/app
CMD ["python", "bot/main.py"]
