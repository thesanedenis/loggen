#!/usr/bin/env python3

import logging
import random
import time

from http.server import BaseHTTPRequestHandler, HTTPServer
from opentelemetry import metrics
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export.controller import PushController
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Генерация трассировки
        with tracer.start_as_current_span("example-handler"):
            logging.info("Handling request...")
            
            # Обработка запроса
            time.sleep(random.random() / 10)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello, World!")

def generate_metrics():
    meter = MeterProvider().get_meter(__name__)
    counter = meter.create_metric("example_counter", "example counter", "1", int, metrics.Counter, ())

    while True:
        # Генерация случайной метрики
        counter.add(1)

        # Задержка перед генерацией следующей метрики
        time.sleep(random.random() / 2)

if __name__ == "__main__":
    # Инициализация экспортера OTLP для передачи данных в OpenTelemetry Collector
    otel_exporter = OTLPSpanExporter(endpoint="opentelemetry-collector-host:4317", insecure=True)
    span_processor = BatchSpanProcessor(otel_exporter)
    tracer_provider = TracerProvider()
    tracer_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(tracer_provider)

    # Инициализация экспортера Prometheus для метрик
    metrics_exporter = PrometheusMetricsExporter()
    controller = PushController(meter_provider=MeterProvider(), exporter=metrics_exporter, interval=5)
    
    # Запуск горутины для генерации метрик
    generate_metrics_thread = threading.Thread(target=generate_metrics)
    generate_metrics_thread.start()

    # Настройка логирования
    logging.basicConfig(level=logging.INFO)

    # Запуск HTTP-сервера
    server = HTTPServer(("localhost", 8080), Handler)
    server.serve_forever()
