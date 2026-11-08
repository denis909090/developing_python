from flask import Flask, request, jsonify, abort
from datetime import datetime

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

students_db = {}
next_id = 1


@app.route("/api/students", methods=["GET"])
def get_students():
    group = request.args.get('group')
    min_gpa = request.args.get('min_gpa', type=float)
    sort_by = request.args.get('sort_by')
    order = request.args.get('order', 'asc')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    filtered = list(students_db.values())

    if group:
        filtered = [s for s in filtered if s.get('group') == group]
    if min_gpa is not None:
        filtered = [s for s in filtered if s.get('gpa', 0) >= min_gpa]

    if sort_by in ['name', 'gpa', 'group']:
        reverse_sort = (order.lower() == 'desc')
        filtered.sort(key=lambda x: x.get(sort_by, ''), reverse=reverse_sort)

    start = (page - 1) * per_page
    end = start + per_page
    paginated = filtered[start:end]

    return jsonify({
        "count": len(filtered),
        "page": page,
        "per_page": per_page,
        "students": paginated
    })


@app.route("/api/students", methods=["POST"])
def create_student():
    global next_id
    data = request.get_json() or {}
    
    name = data.get('name')
    group = data.get('group')
    email = data.get('email')
    gpa = data.get('gpa')

    if not name or not group or not email:
        abort(400, description="Поля name, group та email обов'язкові")
    if gpa is not None and not (0 <= float(gpa) <= 100):
        abort(422, description="GPA має бути в діапазоні 0-100")
    if any(s.get('email') == email for s in students_db.values()):
        abort(400, description="Студент з таким email вже існує")

    student = {
        "id": next_id,
        "name": name,
        "group": group,
        "email": email,
        "gpa": float(gpa) if gpa else 0.0,
        "created_at": datetime.now().isoformat()
    }
    students_db[next_id] = student
    next_id += 1

    return jsonify(student), 201


@app.route("/api/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    """GET /api/students/:id — отримати конкретного студента."""
    student = students_db.get(student_id)
    if not student:
        abort(404)
    return jsonify(student)


@app.route("/api/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """PUT /api/students/:id — повне оновлення студента."""
    student = students_db.get(student_id)
    if not student:
        abort(404)
    
    data = request.get_json() or {}
    if not data.get('name') or not data.get('group') or not data.get('email'):
        abort(400, description="Для повного оновлення потрібні name, group, email")
        
    student.update({
        "name": data['name'],
        "group": data['group'],
        "email": data['email'],
        "gpa": float(data.get('gpa', student.get('gpa', 0)))
    })
    return jsonify(student), 200


@app.route("/api/students/<int:student_id>", methods=["PATCH"])
def patch_student(student_id):
    student = students_db.get(student_id)
    if not student:
        abort(404)

    data = request.get_json() or {}
    if 'name' in data: student['name'] = data['name']
    if 'group' in data: student['group'] = data['group']
    if 'email' in data: student['email'] = data['email']
    if 'gpa' in data: 
        if 0 <= float(data['gpa']) <= 100:
            student['gpa'] = float(data['gpa'])
        else:
            abort(422, description="GPA має бути в діапазоні 0-100")

    return jsonify(student), 200


@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    if student_id not in students_db:
        abort(404)
    del students_db[student_id]
    return '', 204


@app.route("/api/students/stats", methods=["GET"])
def students_stats():
    all_students = list(students_db.values())
    total = len(all_students)
    avg_gpa = sum(s.get('gpa', 0) for s in all_students) / total if total > 0 else 0
    
    groups = {}
    for s in all_students:
        g = s.get('group')
        groups[g] = groups.get(g, 0) + 1
        
    top_students = sorted(all_students, key=lambda x: x.get('gpa', 0), reverse=True)[:3]

    return jsonify({
        "total": total,
        "avg_gpa": round(avg_gpa, 2),
        "groups": groups,
        "top_students": top_students
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ресурс не знайдено", "status": 404}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error.description) if error.description else "Некоректний запит", "status": 400}), 400

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"error": str(error.description) if error.description else "Помилка валідації", "status": 422}), 422


if __name__ == "__main__":
    test_students = [
        {"name": "Іваненко О.", "group": "КІ-21", "email": "ivan@kpi.ua", "gpa": 85.5},
        {"name": "Петренко М.", "group": "КІ-21", "email": "petro@kpi.ua", "gpa": 92.0},
        {"name": "Сидоренко А.", "group": "КІ-22", "email": "syd@kpi.ua", "gpa": 78.3},
        {"name": "Коваль Л.", "group": "КІ-22", "email": "koval@kpi.ua", "gpa": 95.1},
    ]
    for s in test_students:
        students_db[next_id] = {**s, "id": next_id, "created_at": datetime.now().isoformat()}
        next_id += 1

    app.run(debug=True, port=5005)