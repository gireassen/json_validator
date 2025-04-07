FROM python:3.9-alpine AS builder

RUN apk add --no-cache build-base

WORKDIR /app

COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.9-alpine

RUN apk add --no-cache libgcc

WORKDIR /app

COPY --from=builder /root/.local /root/.local

COPY . .

ENV PATH=/root/.local/bin:$PATH

HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8000/ || exit 1

EXPOSE 8000

CMD ["python", "server.py"]