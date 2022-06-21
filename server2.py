import time
import flask
import threading
import requests

stack = []

app = flask.Flask(__name__)

# Entrypoint for put
@app.post("/api/")
def put_func():
    global stack
    # Add the new entry to the back of the stack
    stack.append(flask.request.json)
    return flask.jsonify({"status": "success"})

def stack_extractor():
    global stack
    # Extract the entry from back the stack and send it via a post
    while True:
        if len(stack) > 0:
            last_entry = stack.pop()
            requests.put("http://localhost:5000/api/", json=last_entry)
            time.sleep(1)
        else:
            time.sleep(1)

extractor_threads = 3
extractors = [threading.Thread(target=stack_extractor) for i in range(extractor_threads)]

if __name__ == '__main__':
    for thread in extractors:
        thread.start()
    app.run(host='127.0.0.1', port=5001)
