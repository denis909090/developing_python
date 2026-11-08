from flask import Flask, request, jsonify, abort
from functools import wraps

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

def validate_json(required_fields):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json(silent=True)
            if data is None:
                return jsonify({"error": "Очікується JSON"}), 400
            missing = [field for field in required_fields if field not in data]
            if missing:
                return jsonify({"error": f"Відсутні поля: {', '.join(missing)}"}), 400
            return f(*args, **kwargs)
        return wrapper
    return decorator

items_db = {
    1: {"id": 1, "name": "Ноутбук", "price": 25000, "category": "електроніка"},
    2: {"id": 2, "name": "Книга Python", "price": 500, "category": "книги"},
    3: {"id": 3, "name": "Навушники", "price": 2000, "category": "електроніка"},
}
next_id = 4

@app.route("/api/items", methods=["GET"])
def get_items():
    category = request.args.get("category")
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    sort = request.args.get("sort")
    order = request.args.get("order", "asc")

    results = list(items_db.values())

    if category:
        results = [i for i in results if i["category"] == category]
    if min_price is not None:
        results = [i for i in results if i["price"] >= min_price]
    if max_price is not None:
        results = [i for i in results if i["price"] <= max_price]

    if sort in ["name", "price"]:
        results.sort(key=lambda x: x[sort], reverse=(order == "desc"))

    return jsonify({
        "count": len(results),
        "items": results
    })

@app.route("/api/items", methods=["POST"])
@validate_json(["name", "price", "category"])
def create_item():
    global next_id
    data = request.get_json()
    
    if not isinstance(data["name"], str) or not data["name"].strip():
        return jsonify({"error": "Поле name не може бути порожнім"}), 400
    if not isinstance(data["price"], (int, float)) or data["price"] <= 0:
        return jsonify({"error": "Поле price має бути більшим за 0"}), 400

    new_item = {
        "id": next_id,
        "name": data["name"].strip(),
        "price": data["price"],
        "category": data["category"].strip()
    }
    items_db[next_id] = new_item
    next_id += 1
    return jsonify(new_item), 201

@app.route("/api/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = items_db.get(item_id)
    if not item:
        abort(404)
    return jsonify(item)

@app.route("/api/items/<int:item_id>", methods=["PUT"])
@validate_json(["name", "price", "category"])
def update_item(item_id):
    item = items_db.get(item_id)
    if not item:
        abort(404)
        
    data = request.get_json()
    item["name"] = data["name"]
    item["price"] = data["price"]
    item["category"] = data["category"]
    
    return jsonify(item), 200

@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    if item_id in items_db:
        del items_db[item_id]
        return "", 204
    abort(404)

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ресурс не знайдено"}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Некоректний запит"}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5001)