import os
import sys
#3.1
class Config:
    SECRET_KEY = 'super-secret-key'
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-prod-key')

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}

def create_app(config_name: str = 'default') -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    register_routes(app)
    return app

def register_routes(app: Flask):
    @app.route('/')
    def index():
        return "<h1>Головна Flask</h1><p><a href='/about'>Про додаток</a></p><p><a href='/api/info'>API Info</a></p>"

    @app.route('/about')
    def about():
        return "Це тестовий Flask додаток."

    @app.route('/api/info')
    def api_info():
        return jsonify({
            'framework': 'Flask',
            'version': importlib.import_module('flask').__version__,
            'debug': app.config['DEBUG'],
            'routes': [str(rule) for rule in app.url_map.iter_rules()]
        })

    @app.route('/greet')
    @app.route('/greet/<name>')
    def greet(name=None):
        name = name or request.args.get('name', 'Гість')
        return f"Привіт, {name}!"

# 3.2
def scan_directory(path: str, prefix: str = '') -> list[str]:
    tree = []
    if not os.path.isdir(path): return tree
    
    entries = sorted(os.listdir(path))
    entries = [e for e in entries if e not in ('__pycache__', 'venv', 'db.sqlite3') and not e.endswith('.pyc')]
    
    for i, entry in enumerate(entries):
        is_last = (i == len(entries) - 1)
        connector = '└── ' if is_last else '├── '
        tree.append(f"{prefix}{connector}{entry}")
        full_path = os.path.join(path, entry)
        
        if os.path.isdir(full_path):
            new_prefix = prefix + ('    ' if is_last else '│   ')
            tree.extend(scan_directory(full_path, new_prefix))
    return tree

def analyze_project(path: str) -> dict:
    stats = {'py_files': 0, 'html_files': 0, 'css_files': 0, 'total_size': 0, 'directories': 0}
    if not os.path.isdir(path): return stats

    for root, dirs, files in os.walk(path):
        if '__pycache__' in dirs: dirs.remove('__pycache__')
        if 'venv' in dirs: dirs.remove('venv')
        
        stats['directories'] += len(dirs)
        for file in files:
            if file == 'db.sqlite3' or file.endswith('.pyc'): continue
            
            file_path = os.path.join(root, file)
            stats['total_size'] += os.path.getsize(file_path)
            if file.endswith('.py'): stats['py_files'] += 1
            elif file.endswith('.html'): stats['html_files'] += 1
            elif file.endswith('.css'): stats['css_files'] += 1
            
    return stats

def task_3_2_demo():
    django_path = 'mysite'
    flask_path = 'myflaskapp'

    for path in [django_path, flask_path]:
        if not os.path.isdir(path):
            print(f"Каталог '{path}' не знайдено. Для повноцінного тесту створіть папки проектів")
            return

    print(f"\n Django ({django_path})")
    for line in scan_directory(django_path): print(line)
    d_stats = analyze_project(django_path)

    print(f"\n Flask ({flask_path})")
    for line in scan_directory(flask_path): print(line)
    f_stats = analyze_project(flask_path)

    print("\n| Характеристика   | Django     | Flask      |")
    print(f"| Файли .py        | {d_stats['py_files']:<10} | {f_stats['py_files']:<10} |")
    print(f"| Файли .html      | {d_stats['html_files']:<10} | {f_stats['html_files']:<10} |")
    print(f"| Каталоги         | {d_stats['directories']:<10} | {f_stats['directories']:<10} |")
    print(f"| Розмір (байт)    | {d_stats['total_size']:<10} | {f_stats['total_size']:<10} |")




task_3_2_demo()


