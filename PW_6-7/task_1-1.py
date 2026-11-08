from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)
app.secret_key = "super-secret-key-for-session"

BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>{{ title }}</title></head>
<body>
    <h1>{{ title }}</h1>
    <nav>
        <a href="{{ url_for('index') }}">Головна</a> |
        <a href="{{ url_for('post_list') }}">Публікації</a> |
        <a href="{{ url_for('search') }}">Пошук</a> |
        <a href="{{ url_for('post_create') }}">Створити</a>
    </nav>
    <hr>
    {{ content | safe }}
</body>
</html>
"""

posts_db = [
    {"id": 1, "title": "Вступ до Python", "content": "Python — потужна мова...", "author": "Іван"},
    {"id": 2, "title": "Flask для початківців", "content": "Flask — мікрофреймворк...", "author": "Марія"},
    {"id": 3, "title": "REST API", "content": "REST — архітектурний стиль...", "author": "Петро"},
]
next_id = 4

@app.route("/")
def index():
    return render_template_string(BASE_TEMPLATE, title="Головна", content="<p>Ласкаво просимо на головну сторінку!</p>")

@app.route("/posts")
def post_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    start = (page - 1) * per_page
    end = start + per_page
    
    paginated_posts = posts_db[start:end]
    content = "<ul>"
    for post in paginated_posts:
        content += f"<li><a href='{url_for('post_detail', post_id=post['id'])}'>{post['title']}</a> (Автор: {post['author']})</li>"
    content += "</ul>"
    
    return render_template_string(BASE_TEMPLATE, title="Список публікацій", content=content)

@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    post = next((p for p in posts_db if p["id"] == post_id), None)
    if not post:
        return render_template_string(BASE_TEMPLATE, title="Помилка 404", content="<p>Публікацію не знайдено</p>"), 404
    
    content = f"<h2>{post['title']}</h2><p>{post['content']}</p><p><i>Автор: {post['author']}</i></p>"
    return render_template_string(BASE_TEMPLATE, title=post['title'], content=content)

@app.route("/posts/create", methods=["GET", "POST"])
def post_create():
    global next_id
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        author = request.form.get("author")
        
        if title and content and author:
            posts_db.append({"id": next_id, "title": title, "content": content, "author": author})
            next_id += 1
            return redirect(url_for('post_list'))
            
    form = """
    <form method="POST">
        <label>Заголовок:</label><br><input type="text" name="title" required><br><br>
        <label>Автор:</label><br><input type="text" name="author" required><br><br>
        <label>Зміст:</label><br><textarea name="content" required></textarea><br><br>
        <button type="submit">Зберегти</button>
    </form>
    """
    return render_template_string(BASE_TEMPLATE, title="Створення публікації", content=form)

@app.route("/search")
def search():
    q = request.args.get('q', '').lower()
    results = [p for p in posts_db if q in p['title'].lower() or q in p['content'].lower()] if q else []
    
    content = f"<form method='GET'><input type='text' name='q' value='{q}'><button type='submit'>Шукати</button></form><br>"
    if q:
        content += "<ul>" + "".join(f"<li><a href='{url_for('post_detail', post_id=p['id'])}'>{p['title']}</a></li>" for p in results) + "</ul>"
        if not results:
            content += "<p>Нічого не знайдено.</p>"
            
    return render_template_string(BASE_TEMPLATE, title="Пошук", content=content)

@app.route("/archive/<int:year>/<int:month>")
def archive(year, month):
    content = f"<p>Перегляд архіву за {month:02d}/{year}</p>"
    return render_template_string(BASE_TEMPLATE, title=f"Архів: {year}-{month:02d}", content=content)

@app.route("/user/<username>")
def user_profile(username):
    user_posts = [p for p in posts_db if p['author'].lower() == username.lower()]
    content = f"<h3>Публікації {username}:</h3><ul>"
    content += "".join(f"<li>{p['title']}</li>" for p in user_posts) if user_posts else "<li>Немає публікацій</li>"
    content += "</ul>"
    return render_template_string(BASE_TEMPLATE, title=f"Профіль: {username}", content=content)

if __name__ == "__main__":
    app.run(debug=True, port=5000)