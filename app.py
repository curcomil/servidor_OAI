from flask import Flask, jsonify, request, Response

app = Flask(__name__)

@app.route("/")
def home ():
    app.logger.info(f"Acceso a home")
    return jsonify({"mensaje": "Hola mundo"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)