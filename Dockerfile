FROM python:3.12-slim

WORKDIR /app


COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --timeout 100 --retries 5 -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python" , "app.py"]
