FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install flask prometheus_client jaeger-client opentracing-instrumentation

EXPOSE 5000

CMD ["python", "app.py"]
