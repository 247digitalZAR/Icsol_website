FROM python:3.12-alpine

WORKDIR /app
COPY public /app/public
COPY serve.py /app/serve.py

ENV PORT=3000
EXPOSE 3000

CMD ["sh", "-c", "exec python3 /app/serve.py --port ${PORT:-3000} --directory /app/public"]
