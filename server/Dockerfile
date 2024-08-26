FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# TODO: Just upload what you need here
COPY . /app/

EXPOSE 8000

CMD ["python3", "host.py"]

# docker build -t receipt_service .
# docker run --rm -it -p 8000:8000 receipt_service