# Copyright 2020 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START cloudrun_helloworld_service]
# [START run_helloworld_service]
import os

from flask import Flask

app = Flask(__name__)


@app.route("/")
@app.route("/<name>")
def hello_world(name = "World"):
    return "<H2>Good evening {}!</h2>".format(name)

@app.route("/fuka")
def fuka():
    def fibo2():
        slowfibo(2)
    def fibo10():
        slowfibo(10)
    def fibo20():
        slowfibo(20)
    fibo10
    fibo2
    fibo20
    
def slowfibo(n):
	if n < 2 :
		return n
	return slowfibo(n-2) + slowfibo(n-1)
    
        
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
