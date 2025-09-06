FROM python:3.13-slim

WORKDIR /app

COPY requirements/base.txt ./base.txt
RUN pip install --no-cache-dir -r base.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "2"]
