
import os
from flask import Flask,jsonify
import json
import time

from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.cloud_trace_propagator import (
    CloudTraceFormatPropagator,
)
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
set_global_textmap(CloudTraceFormatPropagator())

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)


tracer_provider = TracerProvider()
cloud_trace_exporter = CloudTraceSpanExporter()
tracer_provider.add_span_processor(
    BatchSpanProcessor(cloud_trace_exporter)
)
trace.set_tracer_provider(tracer_provider)

tracer = trace.get_tracer(__name__)

local_version = "0.01"

@app.route("/")
@app.route("/<name>")
def hello_world(name = "World"):
    print(f"tracer name: {__name__}")
    with tracer.start_as_current_span("hello_world"):
        return "<H2>Hello, {}!</h2>".format(name)


@app.route("/version")
def version():
    return jsonify({"version":local_version})

@app.route("/api")
@app.route("/api/0.02")
def _api():
    from datetime import datetime
    return jsonify({"name":datetime.now().strftime("%Y%m%d-%H:%M:%S")})

@app.route("/fuka")
def fuka():
    def fibo2():
        slowfibo(2)
    def fibo26():
        slowfibo(26)
    def fibo30():
        slowfibo(30)
    t = []
    def _calling(runfunc):
        with tracer.start_as_current_span(runfunc.__name__):
            s = time.process_time()
            start = time.time()
            runfunc()
            end = time.time()
            r = {"name":runfunc.__name__, "elapse":end-start}
            t.append(r)
        return r
    _calling(fibo26)
    _calling(fibo2)
    _calling(fibo30)
    return jsonify(t)
    
def slowfibo(n):
	if n < 2 :
		return n
	return slowfibo(n-2) + slowfibo(n-1)
    
        
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
