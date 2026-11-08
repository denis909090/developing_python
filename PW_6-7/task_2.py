from flask import Flask, request, render_template_string, redirect, url_for, flash, abort
from datetime import datetime

app = Flask(__name__)
app.secret_key = "blog-secret-key"

LIST_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Блог</title></head>
<body>
    <h1>Публікації</h1>
    {% with messages = get_flashed_messages() %}
    {% if messages %}<div style="color: green; font-weight: bold; margin-bottom: 10px;">{{ messages[0] }}</div>{% endif %}
    {% endwith %}
    <a href="{{ url_for('post_create') }}">+ Нова публікація</a>
    <hr>
    {% for post in posts %}
    <article>
        <h2><a href="{{ url_for('post_detail', post_id=post.id) }}">{{ post.title }}</a></h2>
        <p>{{ post.content[:100] }}...</p>
        <small>{{ post.author }} | {{ post.created_at }}</small>
    </article>
    <hr>
    {% else %}
    <p>Поки немає публікацій.</p>
    {% endfor %}
    
    <!-- Проста пагінація -->
    <div>
        {% if page > 1 %}<a href="{{ url_for('post_list', page=page-1) }}">Попередня</a> | {% endif %}
        Сторінка {{ page }}
        <a href="{{ url_for('post_list', page=page+1) }}"> | Наступна</a>
    </div>
</body>
</html>
"""

DETAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>{{ post.title }}</title></head>
<body>
    <h1>{{ post.title }}</h1>
    {% with messages = get_flashed_messages() %}
    {% if messages %}<div style="color: green; font-weight: bold;">{{ messages[0] }}</div>{% endif %}
    {% endwith %}
    <p><i>Автор: {{ post.author }} | Дата: {{ post.created_at }}</i></p>
    <hr>
    <p>{{ post.content }}</p>
    <a href="{{ url_for('post_list') }}">← Назад до списку</a>
</body>
</html>
"""

FORM_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>{{ form_title }}</title></head>
<body>
    <h1>{{ form_title }}</h1>
    {% with messages = get_flashed_messages() %}
    {% if messages %}<div style="color: red; margin-bottom: 10px;">{{ messages[0] }}</div>{% endif %}
    {% endwith %}
    <form method="POST">
        <label>Заголовок:</label><br>
        <input type="text" name="title" value="{{ post.title if post else '' }}" required style="width:400px;"><br><br>
        <label>Автор:</label><br>
        <input type="text" name="author" value="{{ post.author if post else '' }}" required><br><br>
        <label>Зміст:</label><br>
        <textarea name="content" rows="10" cols="50" required>{{ post.content if post else '' }}</textarea><br><br>
        <button type="submit">{{ button_text }}</button>
        <a href="{{ url_for('post_list') }}">Скасувати</a>
    </form>
</body>
</html>
"""

posts_db = []
next_id = 1

@app.route("/")
@app.route("/posts")
def post_list():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    start = (page - 1) * per_page
    end = start + per_page
    
    paginated_posts = posts_db[start:end]
    return render_template_string(LIST_TEMPLATE, posts=paginated_posts, page=page)

@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    post = next((p for p in posts_db if p["id"] == post_id), None)
    if not post:
        abort(404)
    return render_template_string(DETAIL_TEMPLATE, post=post)

@app.route("/posts/create", methods=["GET", "POST"])
def post_create():
    global next_id
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        content = request.form.get("content", "").strip()
        
        # Серверна валідація
        if not title or not author or not content:
            flash("Всі поля є обов'язковими для заповнення!")
        else:
            new_post = {
                "id": next_id,
                "title": title,
                "author": author,
                "content": content,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            posts_db.append(new_post)
            next_id += 1
            flash("Публікацію успішно створено!")
            return redirect(url_for('post_detail', post_id=new_post["id"]))
            
    return render_template_string(FORM_TEMPLATE, form_title="Нова публікація", button_text="Створити", post=None)

if __name__ == "__main__":
    app.run(debug=True, port=5003)