from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def home():
    return jsonify({"message": "Python CI/CD Demo API is running!"})

@app.get("/hello/<name>")
def greet(name):
    return jsonify({"greeting": f"Hello, {name}!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
