from flask import Flask, request, jsonify

app = Flask(__name__)
API_KEY = '123'

requests = []

def verify_api_key(request):
    api_key = request.headers.get('Authorization')
    if api_key and api_key == API_KEY:
        return True
    return False

@app.route("/client/status", methods=['GET'])
def status():
    if not verify_api_key(request):
        return jsonify({'error': 'Unauthorized'}), 401
    
    if not requests:
        return jsonify("No order is set yet!"), 200
    
    last_order = requests[-1]
    lamp_status = "Lamp is ON" if last_order == "ON" else "Lamp is OFF"
    return jsonify(lamp_status)

@app.route("/client/requests", methods=['POST'])
def add_req():
    if not verify_api_key(request):
        return jsonify({'error': 'Unauthorized'}), 401
    
    order = request.json.get('order')
    if order not in ("ON", "OFF"):
        return
    requests.append(order)
    return jsonify("Turned "+ order), 200

if __name__ == '__main__':
    app.run(debug=True)
