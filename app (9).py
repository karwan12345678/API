from flask import Flask, request, jsonify


app = Flask(__name__)

requests = []

@app.get("/client/status")
def status():
    def is_lamp_on():
        last = requests[-1]
        if last == "on":
            return 1
        else:
            return 0
    try:
        if is_lamp_on():
            return jsonify({"status": "Lamp is on"})
        else:
            return jsonify({"status": "Lamp is off"})
    except IndexError:
        return jsonify({"error": "you didnt set any order yet"}), 400    


@app.post("/client/requests")
def add_req():
    order = request.form.get('order')
    if order not in ("on", "off"):
        return jsonify({"error": "Invalid order. You can only use 'on' or 'off'."}), 400
    requests.append(order)
    return jsonify({"message": "Order added successfully"}), 201


if __name__ == '__main__':
    app.run(debug=True)
