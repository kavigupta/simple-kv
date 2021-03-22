from flask import Flask, request


from store import store

app = Flask(__name__)


@app.route("/get", methods=["GET"])
def get():
    api_key = request.args["api_key"]
    key = request.args["k"]
    s = store(api_key)
    if s is None:
        return f"Error, key {api_key} was invalid", 403
    value = s.get(key)
    if value is None:
        return f"Error, key {key} not found in database", 404
    return value, 200


@app.route("/put", methods=["POST"])
def put():
    s = store(request.args["api_key"])
    if s is None:
        return f"Error, key {request.args['api_key']} was invalid", 403
    key, value = request.args["k"], request.data
    value = value.decode("utf-8")
    method = request.args.get("method", "replace")

    if method == "replace":
        s.put(key, value)
    elif method == "append":
        s.append(key, value)
    else:
        return f"Invalid method: {method}", 400
    return f"Success", 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
