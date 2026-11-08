import sys
import importlib
import subprocess
import os
import json
# from flask import Flask, jsonify, request

# 1.1
def check_python_version():
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("nреба Python 3.10 або новіше")

def check_package(package_name: str) -> bool:
    try:
        module = importlib.import_module(package_name)
        version = getattr(module, '__version__', 'невідома')
        print(f"  {package_name}: {version}")
        return True
    except ImportError:
        print(f"  {package_name}: НЕ ВСТАНОВЛЕНО")
        return False

def task_1_1_demo():
    check_python_version()
    print("\nВстановлені пакети:")
    packages = ['django', 'flask']
    results = {pkg: check_package(pkg) for pkg in packages}
    
    installed = sum(results.values())
    missing = len(packages) - installed
    print(f"\nПідсумок: Встановлено - {installed}, Відсутні - {missing}")
    
    missing_pkgs = [pkg for pkg, is_inst in results.items() if not is_inst]
    if missing_pkgs:
        print(f"Для встановлення виконайте: pip install {' '.join(missing_pkgs)}")

# 1.2
def get_installed_packages() -> list[dict]:
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'list', '--format=json'],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        return json.loads(result.stdout)
    return []

def generate_requirements(packages: list[dict], filename: str = 'requirements.txt'):
    sys_pkgs = {'pip', 'setuptools', 'wheel'}
    with open(filename, 'w') as f:
        for pkg in packages:
            if pkg['name'].lower() not in sys_pkgs:
                f.write(f"{pkg['name']}=={pkg['version']}\n")

def verify_requirements(filename: str = 'requirements.txt') -> bool:
    if not os.path.exists(filename):
        return False
    
    installed = {p['name'].lower(): p['version'] for p in get_installed_packages()}
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                name, version = line.strip().split('==')
                if name.lower() not in installed or installed[name.lower()] != version:
                    return False
    return True

def task_1_2_demo():
    packages = get_installed_packages

task_1_1_demo()
task_1_2_demo()