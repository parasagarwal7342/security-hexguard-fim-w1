from flask import Flask, render_template, request, jsonify
import os
import sys
# Add src to path if needed
sys.path.append(os.path.abspath("src"))
from integrity_checker import IntegrityChecker

app = Flask(__name__)

# Basic configuration
WATCH_DIR = "sample_input"
BASELINE_FILE = "baseline.json"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    data = request.json
    target = data.get("target", WATCH_DIR)
    if not os.path.isdir(target):
        return jsonify({"error": "Target path not found/invalid"}), 400
        
    checker = IntegrityChecker(target)
    baseline_path = os.path.join(target, BASELINE_FILE)
    if not os.path.exists(baseline_path):
        checker.generate_baseline(baseline_path)
        return jsonify({"status": "initialized", "message": "First-time baseline created for " + target})
        
    results = checker.verify_integrity(baseline_path)
    return jsonify(results)

@app.route("/heal", methods=["POST"])
def heal():
    data = request.json
    target = data.get("target", WATCH_DIR)
    filename = data.get("filename")
    checker = IntegrityChecker(target)
    success = checker.restore_file(filename)
    return jsonify({"success": success})

@app.route("/init", methods=["POST"])
def initialize():
    data = request.json
    target = data.get("target", WATCH_DIR)
    if not os.path.isdir(target):
        return jsonify({"error": "Target path not found/invalid"}), 400
    checker = IntegrityChecker(target)
    baseline_path = os.path.join(target, BASELINE_FILE)
    checker.generate_baseline(baseline_path)
    return jsonify({"status": "success", "message": "Secure Vault Synchronized for " + target})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
