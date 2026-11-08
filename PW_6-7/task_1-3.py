from flask import Flask, request, make_response, session, redirect, url_for, jsonify

app = Flask(__name__)
app.secret_key = "super-secret-key-for-session"

products_db = {
    1: {"name": "Ноутбук", "price": 25000},
    2: {"name": "Смартфон", "price": 12000},
    3: {"name": "Навушники", "price": 2000},
}

@app.route("/set-theme/<theme>")
def set_theme(theme):
    resp = make_response(jsonify({"message": f"Тему {theme} встановлено"}))
    resp.set_cookie("theme", theme, max_age=30*24*60*60, httponly=True, samesite='Lax')
    return resp

@app.route("/get-theme")
def get_theme():
    theme = request.cookies.get("theme", "light")
    return jsonify({"theme": theme})

@app.route("/set-language/<lang>")
def set_language(lang):
    resp = make_response(jsonify({"message": f"Мову {lang} встановлено"}))
    resp.set_cookie("language", lang, max_age=30*24*60*60, httponly=True, samesite='Lax')
    return resp

@app.route("/preferences")
def preferences():
    return jsonify(dict(request.cookies))

@app.route("/cart/add/<int:product_id>")
def add_to_cart(product_id):
    if product_id not in products_db:
        return jsonify({"error": "Товар не знайдено"}), 404
        
    if "cart" not in session:
        session["cart"] = []
        
    session["cart"].append(product_id)
    session.modified = True
    return jsonify({"message": f"Товар {product_id} додано", "cart": session["cart"]})

@app.route("/cart")
def view_cart():
    cart_ids = session.get("cart", [])
    items = [products_db[pid] for pid in cart_ids if pid in products_db]
    total = sum(item["price"] for item in items)
    return jsonify({"cart_items": items, "total": total})

@app.route("/cart/clear")
def clear_cart():
    session.pop("cart", None)
    return jsonify({"message": "Кошик очищено"})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or request.form
    username = data.get("username")
    if username:
        session["username"] = username
        return jsonify({"message": f"Користувач {username} увійшов"})
    return jsonify({"error": "Не вказано username"}), 400

@app.route("/logout")
def logout():
    session.pop("username", None)
    return jsonify({"message": "Вихід виконано"})

@app.route("/profile")
def profile():
    if "username" not in session:
        return jsonify({"error": "Необхідна авторизація"}), 401
    return jsonify({"message": f"Профіль {session['username']}"})

if __name__ == "__main__":
    app.run(debug=True, port=5002)