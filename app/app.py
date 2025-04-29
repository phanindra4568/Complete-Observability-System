from flask import Flask
import time, logging
from prometheus_client import Counter, generate_latest
from jaeger_client import Config
from opentracing_instrumentation.client_hooks import install_all_patches

app = Flask(__name__)
install_all_patches()

# Logging
logging.basicConfig(level=logging.INFO)

# Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests')

# Tracing
def init_tracer(service):
    config = Config(config={'sampler': {'type': 'const', 'param': 1},
                            'logging': True}, service_name=service)
    return config.initialize_tracer()

tracer = init_tracer('demo-app')

@app.route("/")
def hello():
    REQUEST_COUNT.inc()
    with tracer.start_span('hello-span'):
        logging.info("Hit / endpoint")
        time.sleep(0.5)
        return "Hello, Observability!"

@app.route("/metrics")
def metrics():
    return generate_latest()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
