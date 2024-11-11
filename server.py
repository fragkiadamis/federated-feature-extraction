from flask import Flask, request, jsonify

app = Flask(__name__)

# Placeholder for received features
features_list = []


# Endpoint to receive features from nodes
@app.route('/upload', methods=['POST'])
def receive_features():
    data = request.get_json()
    client_id = data.get("client_id")
    features = data.get("features")

    if features:
        print(client_id, features)
        return jsonify({"status": "received"})
    else:
        return jsonify({"status": "error", "message": "No features received"}), 400


# Run the server
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)