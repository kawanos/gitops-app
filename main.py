
import os

from flask import Flask,jsonify
import json

app = Flask(__name__)

local_version = "0.01"

@app.route("/")
@app.route("/<name>")
def hello_world(name = "World"):
    return "<H2>こんにちわ {}!</h2>".format(name)


@app.route("/version")
def version():
    return jsonify({"version":local_version})

@app.route("/fuka")
def fuka():
    def fibo2():
        slowfibo(2)
    def fibo20():
        slowfibo(20)
    def fibo30():
        slowfibo(30)
    t = []
    def _calling(runfunc):
        import time
        s = time.process_time()
        start = time.time()
        runfunc()
        end = time.time()
        r = {"name":runfunc.__name__, "elapse":end-start}
        t.append(r)
        return r
    _calling(fibo20)
    _calling(fibo2)
    _calling(fibo30)
    return jsonify(t)
    
def slowfibo(n):
	if n < 2 :
		return n
	return slowfibo(n-2) + slowfibo(n-1)
    
        
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))