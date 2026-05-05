from flask import Flask, render_template, request, jsonify
import importlib.util
import os

brain = None
brain_path = os.path.join(os.path.dirname(__file__), "brain.py")
if os.path.exists(brain_path):
    spec = importlib.util.spec_from_file_location("brain", brain_path)
    brain = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(brain)
else:
    class _BrainFallback:
        @staticmethod
        def generate_response(message):
            return "Sorry, I cannot respond right now."
    brain = _BrainFallback()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message")
    response = brain.generate_response(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
