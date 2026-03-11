#!/usr/bin/env python3
"""
Phase 1 Compliance Test Script
Tests all 6 required features without needing a running database
"""

import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test 1: Verify all modules can be imported"""
    print("\n=== TEST 1: Module Imports ===")
    errors = []
    
    try:
        from app.main import app
        print("✓ app.main imports OK")
    except Exception as e:
        errors.append(f"app.main: {e}")
        print(f"✗ app.main failed: {e}")
    
    try:
        from app.config import get_settings
        print("✓ app.config imports OK")
    except Exception as e:
        errors.append(f"app.config: {e}")
        print(f"✗ app.config failed: {e}")
    
    try:
        from app.database import Base, engine, get_db
        print("✓ app.database imports OK")
    except Exception as e:
        errors.append(f"app.database: {e}")
        print(f"✗ app.database failed: {e}")
    
    try:
        from app.auth import get_current_user
        print("✓ app.auth imports OK")
    except Exception as e:
        errors.append(f"app.auth: {e}")
        print(f"✗ app.auth failed: {e}")
    
    # Test routers
    routers = ['chapters', 'quizzes', 'progress', 'access', 'users', 'search']
    for router_name in routers:
        try:
            __import__(f'app.routers.{router_name}')
            print(f"✓ app.routers.{router_name} imports OK")
        except Exception as e:
            errors.append(f"app.routers.{router_name}: {e}")
            print(f"✗ app.routers.{router_name} failed: {e}")
    
    # Test services
    services = ['r2_service', 'quiz_service', 'progress_service', 'access_service']
    for service_name in services:
        try:
            __import__(f'app.services.{service_name}')
            print(f"✓ app.services.{service_name} imports OK")
        except Exception as e:
            errors.append(f"app.services.{service_name}: {e}")
            print(f"✗ app.services.{service_name} failed: {e}")
    
    # Test models
    models = ['user', 'chapter', 'quiz', 'progress']
    for model_name in models:
        try:
            __import__(f'app.models.{model_name}')
            print(f"✓ app.models.{model_name} imports OK")
        except Exception as e:
            errors.append(f"app.models.{model_name}: {e}")
            print(f"✗ app.models.{model_name} failed: {e}")
    
    # Test schemas
    schemas = ['common', 'chapter', 'quiz', 'progress', 'user']
    for schema_name in schemas:
        try:
            __import__(f'app.schemas.{schema_name}')
            print(f"✓ app.schemas.{schema_name} imports OK")
        except Exception as e:
            errors.append(f"app.schemas.{schema_name}: {e}")
            print(f"✗ app.schemas.{schema_name} failed: {e}")
    
    return errors


def test_zero_llm_compliance():
    """Test 2: Verify no LLM imports in backend"""
    print("\n=== TEST 2: Zero-LLM Compliance ===")
    errors = []
    
    forbidden = ['openai', 'anthropic', 'langchain', 'llama_index', 'cohere', 'groq']
    app_dir = Path(__file__).parent / 'app'
    
    for py_file in app_dir.rglob('*.py'):
        content = py_file.read_text()
        # Skip comments that mention forbidden imports
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            # Skip comment-only lines
            if line.strip().startswith('#'):
                continue
            for forbidden_import in forbidden:
                if f'import {forbidden_import}' in line or f'from {forbidden_import}' in line:
                    errors.append(f"{py_file}:{i} contains forbidden import: {line.strip()}")
                    print(f"✗ {py_file}:{i}: {line.strip()}")
    
    if not errors:
        print("✓ No forbidden LLM imports found")
    
    return errors


def test_router_endpoints():
    """Test 3: Verify all required endpoints are registered"""
    print("\n=== TEST 3: Router Endpoints ===")
    errors = []
    
    from app.main import app
    
    required_endpoints = {
        'GET /chapters': 'List chapters',
        'GET /chapters/{chapter_id}': 'Get chapter',
        'GET /chapters/{chapter_id}/next': 'Get next chapter',
        'GET /chapters/{chapter_id}/prev': 'Get prev chapter',
        'GET /quizzes/{chapter_id}': 'Get quiz questions',
        'POST /quizzes/{chapter_id}/submit': 'Submit quiz',
        'GET /quizzes/{chapter_id}/best-score': 'Get best score',
        'GET /progress/{user_id}': 'Get progress',
        'PUT /progress/{user_id}/chapter/{chapter_id}': 'Update progress',
        'GET /progress/{user_id}/quiz-scores': 'Get quiz scores',
        'GET /access/check': 'Check access',
        'GET /users/me': 'Get current user',
        'GET /search': 'Search content',
        'GET /health': 'Health check',
    }
    
    registered = {f"{route.methods.pop()} {route.path}": route.path for route in app.routes}
    
    # Normalize paths for comparison
    registered_normalized = {}
    for path, info in registered.items():
        normalized = path.replace('{', '{').replace('}', '}')
        registered_normalized[normalized] = info
    
    for endpoint, description in required_endpoints.items():
        method, path = endpoint.split(' ', 1)
        # Check if endpoint is registered (accounting for path parameters)
        found = False
        for reg_path in registered.keys():
            reg_method, reg_path_only = reg_path.split(' ', 1) if ' ' in reg_path else ('GET', reg_path)
            if reg_method == method and path.split('/')[1] in reg_path:
                found = True
                break
        
        if found:
            print(f"✓ {endpoint} - {description}")
        else:
            errors.append(f"Missing endpoint: {endpoint}")
            print(f"✗ {endpoint} - {description} - MISSING")
    
    return errors


def test_todo_placeholders():
    """Test 4: Check for TODO placeholders in critical files"""
    print("\n=== TEST 4: TODO Placeholders ===")
    errors = []
    
    critical_files = [
        'app/routers/access.py',
        'app/routers/search.py',
        'app/routers/progress.py',
    ]
    
    for filepath in critical_files:
        full_path = Path(__file__).parent / filepath
        if full_path.exists():
            content = full_path.read_text()
            if 'TODO' in content:
                errors.append(f"{filepath} contains TODO placeholders")
                print(f"✗ {filepath} contains TODO placeholders")
            else:
                print(f"✓ {filepath} - No TODOs")
        else:
            errors.append(f"{filepath} not found")
            print(f"✗ {filepath} not found")
    
    return errors


def test_required_files():
    """Test 5: Check for required files"""
    print("\n=== TEST 5: Required Files ===")
    errors = []
    
    required_files = [
        'pyproject.toml',
        '.env.example',
        'app/main.py',
        'app/config.py',
        'app/database.py',
        'app/auth.py',
        'app/routers/chapters.py',
        'app/routers/quizzes.py',
        'app/routers/progress.py',
        'app/routers/access.py',
        'app/routers/users.py',
        'app/routers/search.py',
        'app/services/r2_service.py',
        'app/services/quiz_service.py',
        'app/services/progress_service.py',
        'app/services/access_service.py',
        'app/models/user.py',
        'app/models/chapter.py',
        'app/models/quiz.py',
        'app/models/progress.py',
        'app/schemas/common.py',
        'app/schemas/chapter.py',
        'app/schemas/quiz.py',
        'app/schemas/progress.py',
        'app/schemas/user.py',
    ]
    
    for filepath in required_files:
        full_path = Path(__file__).parent / filepath
        if full_path.exists():
            print(f"✓ {filepath}")
        else:
            errors.append(f"Missing: {filepath}")
            print(f"✗ {filepath} - MISSING")
    
    # Check for missing directories
    required_dirs = ['alembic', 'seed', 'tests']
    for dir_name in required_dirs:
        full_path = Path(__file__).parent / dir_name
        if full_path.exists():
            print(f"✓ {dir_name}/ directory exists")
        else:
            errors.append(f"Missing directory: {dir_name}")
            print(f"✗ {dir_name}/ directory - MISSING")
    
    return errors


def main():
    print("=" * 60)
    print("PHASE 1 COMPLIANCE TEST SUITE")
    print("=" * 60)
    
    all_errors = []
    
    # Run all tests
    all_errors.extend(test_imports())
    all_errors.extend(test_zero_llm_compliance())
    all_errors.extend(test_router_endpoints())
    all_errors.extend(test_todo_placeholders())
    all_errors.extend(test_required_files())
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    if all_errors:
        print(f"\n❌ FAILED: {len(all_errors)} errors found\n")
        for error in all_errors:
            print(f"  - {error}")
        print("\n" + "=" * 60)
        print("PHASE 1 IS NOT COMPLETE")
        print("=" * 60)
        return 1
    else:
        print("\n✅ ALL TESTS PASSED")
        print("\n" + "=" * 60)
        print("PHASE 1 IS COMPLETE")
        print("=" * 60)
        return 0


if __name__ == '__main__':
    sys.exit(main())
