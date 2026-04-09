#!/usr/bin/env python3
"""
Script de verificação pós-reorganização CENY
Verifica se todas as mudanças foram aplicadas corretamente
"""

import os
import sys

def check_structure():
    """Verifica a estrutura de diretórios"""
    print("\n📁 VERIFICANDO ESTRUTURA DE DIRETÓRIOS\n")
    
    checks = [
        ("school-management/ceny-vue existe", os.path.isdir("school-management/ceny-vue")),
        ("school-management/ceny-vue/src existe", os.path.isdir("school-management/ceny-vue/src")),
        ("maintenance/ existe", os.path.isdir("maintenance")),
        ("db.sqlite3 existe", os.path.isfile("db.sqlite3")),
    ]
    
    for name, result in checks:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    return all(result for _, result in checks)

def check_files():
    """Verifica arquivos principais"""
    print("\n📄 VERIFICANDO ARQUIVOS PRINCIPAIS\n")
    
    files = [
        "app/settings.py",
        "app/urls.py",
        "school-management/ceny-vue/src/App.vue",
        "school-management/ceny-vue/src/views/HomeView.vue",
        "school-management/ceny-vue/src/router/index.js",
        "school-management/ceny-vue/package.json",
        "school-management/ceny-vue/index.html",
        "CENY_README.md",
        "CENY_API_EXEMPLOS.md",
        "UPGRADE.md",
        "RESUMO_MUDANCAS.md",
    ]
    
    results = []
    for filepath in files:
        exists = os.path.isfile(filepath)
        status = "✅" if exists else "❌"
        results.append(exists)
        print(f"{status} {filepath}")
    
    return all(results)

def check_content():
    """Verifica conteúdo de arquivos chave"""
    print("\n🔍 VERIFICANDO CONTEÚDO DOS ARQUIVOS\n")
    
    checks = []
    
    # Verifica settings.py
    try:
        with open("app/settings.py", "r") as f:
            content = f.read()
            has_students = "'students'" in content
            has_maintenance = "'maintenance'" in content
            checks.append(("settings.py sem 'students'", not has_students))
            checks.append(("settings.py com 'maintenance'", has_maintenance))
    except:
        checks.append(("settings.py verificável", False))
    
    # Verifica urls.py
    try:
        with open("app/urls.py", "r") as f:
            content = f.read()
            has_students_url = "StudentCreateListView" in content
            has_maintenance_url = "maintenance" in content
            checks.append(("urls.py sem StudentCreateListView", not has_students_url))
            checks.append(("urls.py com maintenance", has_maintenance_url))
    except:
        checks.append(("urls.py verificável", False))
    
    # Verifica package.json
    try:
        with open("school-management/ceny-vue/package.json", "r") as f:
            content = f.read()
            has_ceny_name = "ceny-management" in content
            checks.append(("package.json renomeado para ceny-management", has_ceny_name))
    except:
        checks.append(("package.json verificável", False))
    
    # Verifica index.html
    try:
        with open("school-management/ceny-vue/index.html", "r") as f:
            content = f.read()
            has_ceny_title = "CENY" in content
            checks.append(("index.html tem título CENY", has_ceny_title))
    except:
        checks.append(("index.html verificável", False))
    
    for name, result in checks:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    return all(result for _, result in checks)

def print_summary(all_ok):
    """Imprime resumo final"""
    print("\n" + "="*60)
    if all_ok:
        print("✅ TODAS AS VERIFICAÇÕES PASSARAM COM SUCESSO!")
        print("\n🚀 Projeto está pronto para uso:")
        print("   Backend: python manage.py runserver")
        print("   Frontend: cd school-management/ceny-vue && npm run dev")
    else:
        print("⚠️  ALGUMAS VERIFICAÇÕES FALHARAM")
        print("   Revise os arquivos acima")
    print("="*60 + "\n")

def main():
    print("""
╔════════════════════════════════════════════╗
║   🔧 CENY - Verificação Pós-Reorganização  ║
╚════════════════════════════════════════════╝
    """)
    
    try:
        struct_ok = check_structure()
        files_ok = check_files()
        content_ok = check_content()
        
        all_ok = struct_ok and files_ok and content_ok
        print_summary(all_ok)
        
        return 0 if all_ok else 1
    
    except Exception as e:
        print(f"\n❌ Erro durante verificação: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
