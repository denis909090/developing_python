from flask import Flask, request, jsonify, g
from datetime import datetime
from functools import wraps
import time

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


class APIError(Exception):
    def __init__(self, message: str, status_code: int = 400, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}


@app.errorhandler(APIError)
def handle_api_error(error):
    response = {
        "error": error.message,
        "status": error.status_code,
        "details": error.details,
        "timestamp": datetime.now().isoformat(),
    }
    return jsonify(response), error.status_code


# --- Серіалізатор ---

class StudentSerializer:

    @staticmethod
    def serialize(student: dict, fields: list[str] | None = None) -> dict:
        
        if not fields:
            return student
        return {key: value for key, value in student.items() if key in fields}

    @staticmethod
    def deserialize(data: dict) -> dict:
        errors = {}
        
        name = data.get("name")
        if not name:
            errors["name"] = "Поле 'name' є обов'язковим"
            
        group = data.get("group")
        if not group:
            errors["group"] = "Поле 'group' є обов'язковим"
            
        gpa = data.get("gpa")
        if gpa is not None:
            try:
                gpa = float(gpa)
                if not (0 <= gpa <= 100):
                    errors["gpa"] = "GPA має бути від 0 до 100"
                data["gpa"] = gpa
            except ValueError:
                errors["gpa"] = "GPA має бути числом"

        if errors:
            raise APIError("Помилка валідації", status_code=422, details=errors)
            
        return data

    @staticmethod
    def serialize_list(students: list[dict], fields: list[str] | None = None) -> list[dict]:
        
        return [StudentSerializer.serialize(s, fields) for s in students]

@app.before_request
def log_request():
    g.start_time = time.time()
    print(f"[{datetime.now().isoformat()}] INCOMING REQUEST: {request.method} {request.url}")

@app.after_request
def add_headers(response):
    if hasattr(g, 'start_time'):
        duration = time.time() - g.start_time
        response.headers["X-Request-Time"] = f"{duration:.4f}s"
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


def require_api_key(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        if api_key != "secret-api-key-123":
            raise APIError("Невірний або відсутній API-ключ", status_code=401)
        return f(*args, **kwargs)
    return wrapper


students_db = {}
next_id = 1

@app.route("/api/v2/students", methods=["GET"])
def get_students_v2():
    """GET /api/v2/students — з серіалізацією та вибором полів."""
    fields_query = request.args.get('fields')
    fields = fields_query.split(',') if fields_query else None
    search = request.args.get('search', '').lower()
    sort_by = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')

    filtered = list(students_db.values())

    if search:
        filtered = [s for s in filtered if search in s.get('name', '').lower() or search in s.get('group', '').lower()]

    reverse = (order == 'desc')
    filtered.sort(key=lambda x: x.get(sort_by, ''), reverse=reverse)

    serialized_data = StudentSerializer.serialize_list(filtered, fields)
    return jsonify(serialized_data)


@app.route("/api/v2/students", methods=["POST"])
@require_api_key
def create_student_v2():
    global next_id
    data = request.get_json() or {}
    
    clean_data = StudentSerializer.deserialize(data)
    
    email = clean_data.get("email", f"student{next_id}@kpi.ua")
    if any(s.get('email') == email for s in students_db.values()):
        raise APIError("Студент з таким email вже існує", status_code=400)

    student = {
        "id": next_id,
        "name": clean_data["name"],
        "group": clean_data["group"],
        "email": email,
        "gpa": clean_data.get("gpa", 0.0),
        "created_at": datetime.now().isoformat()
    }
    
    students_db[next_id] = student
    next_id += 1

    return jsonify(student), 201


if __name__ == "__main__":
    students_db[next_id] = {"id": next_id, "name": "Тест Тестович", "group": "КІ-21", "email": "test@kpi.ua", "gpa": 90.0, "created_at": datetime.now().isoformat()}
    next_id += 1
    
    app.run(debug=True, port=5006)