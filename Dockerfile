FROM python:3.12-slim

ENV TERM=xterm

WORKDIR /app

COPY . .

CMD ["python3", "main.py"]
