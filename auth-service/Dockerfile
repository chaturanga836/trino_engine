FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY ./app ./app
COPY .env ./  
COPY appprestart.py ./
# Expose port
EXPOSE 7000

# Run FastAPI with Uvicorn
CMD python3 prestart.py && uvicorn app.main:app --host 0.0.0.0 --port 7000
