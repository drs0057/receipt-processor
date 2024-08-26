FROM python:3.11-slim

WORKDIR /app

# pip install first so that future images can rebuild off the same requirements
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY receipt_processor/ /app/receipt_processor
COPY host.py /app/

EXPOSE 8000

CMD ["python3", "host.py"]
