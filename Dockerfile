# Build stage
FROM docker.arvancloud.ir/python:3.13 AS builder
WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip && pip install -r requirements.txt

# Final stage
FROM docker.arvancloud.ir/python:3.13-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY . /app
EXPOSE 8000
CMD ["gunicorn", "contentcritic.wsgi:application", "--bind", "0.0.0.0:8000"]