FROM python:3.13-slim-bookworm as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


FROM python:3.13-slim-bookworm

WORKDIR /app


COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages

COPY . .

ENV PORT 8080
EXPOSE ${PORT}

# Cloud Run은 PORT 환경 변수로 포트를 전달합니다 (기본값 8080).
# uvicorn이 0.0.0.0으로 실행되어야 Cloud Run 환경에서 요청을 받을 수 있습니다.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT}"]
