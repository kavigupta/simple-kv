from flask import Flask, request


from store import store

app = Flask(__name__)


@app.route("/get", methods=["GET"])
def get():
    s = store(request.args["api_key"])
    if s is None:
        return f"Error, key {request.args['api_key']} was invalid", 403
    if request.args["k"] not in s:
        return f"Error, key {request.args['key']} not found in database", 404
    return s[request.args["k"]], 200


@app.route("/put", methods=["POST"])
def put():
    s = store(request.args["api_key"])
    if s is None:
        return f"Error, key {request.args['api_key']} was invalid", 403
    key, value = request.args["k"], request.data
    method = request.args.get("method", "replace")
    if method == "replace":
        s[key] = value
    elif method == "append":
        s[key] += value
    else:
        return f"Invalid method: {method}", 400
    return f"Success, there are now {len(s)} keys", 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
