#!/usr/bin/env python
"""
Script para carregar dados iniciais no banco de dados CENY
Uso: python manage.py shell < load_initial_data.py
Ou: python load_initial_data.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from maintenance.models import Empresa, Setor, Equipamento, OrdemServico
from django.utils import timezone

# Limpar dados existentes (opcional)
# Empresa.objects.all().delete()

print("🔧 Carregando dados iniciais do CENY...\n")

try:
    # Criar Empresas
    print("📦 Criando empresas...")
    empresa1, created = Empresa.objects.get_or_create(
        nome="Indústria XYZ Ltda"
    )
    print(f"  ✓ {empresa1.nome} {'(novo)' if created else '(existente)'}")

    empresa2, created = Empresa.objects.get_or_create(
        nome="Manufatura ABC S.A."
    )
    print(f"  ✓ {empresa2.nome} {'(novo)' if created else '(existente)'}\n")

    # Criar Setores
    print("🏭 Criando setores...")
    setor1, created = Setor.objects.get_or_create(
        nome="Usinagem",
        empresa=empresa1
    )
    print(f"  ✓ {setor1.nome} - {setor1.empresa.nome} {'(novo)' if created else '(existente)'}")

    setor2, created = Setor.objects.get_or_create(
        nome="Montagem",
        empresa=empresa1
    )
    print(f"  ✓ {setor2.nome} - {setor2.empresa.nome} {'(novo)' if created else '(existente)'}")

    setor3, created = Setor.objects.get_or_create(
        nome="Soldagem",
        empresa=empresa2
    )
    print(f"  ✓ {setor3.nome} - {setor3.empresa.nome} {'(novo)' if created else '(existente)'}\n")

    # Criar Equipamentos
    print("⚙️  Criando equipamentos...")
    eq1, created = Equipamento.objects.get_or_create(
        tag="EQ-001",
        defaults={"nome": "Torno CNC Horizontal", "status": "operacional", "setor": setor1}
    )
    print(f"  ✓ {eq1.tag} - {eq1.nome} {'(novo)' if created else '(existente)'}")

    eq2, created = Equipamento.objects.get_or_create(
        tag="EQ-002",
        defaults={"nome": "Centro de Usinagem Vertical", "status": "operacional", "setor": setor1}
    )
    print(f"  ✓ {eq2.tag} - {eq2.nome} {'(novo)' if created else '(existente)'}")

    eq3, created = Equipamento.objects.get_or_create(
        tag="EQ-003",
        defaults={"nome": "Fresadora Universal", "status": "manutencao", "setor": setor1}
    )
    print(f"  ✓ {eq3.tag} - {eq3.nome} {'(novo)' if created else '(existente)'}")

    eq4, created = Equipamento.objects.get_or_create(
        tag="EQ-004",
        defaults={"nome": "Robô Manipulador", "status": "operacional", "setor": setor2}
    )
    print(f"  ✓ {eq4.tag} - {eq4.nome} {'(novo)' if created else '(existente)'}")

    eq5, created = Equipamento.objects.get_or_create(
        tag="EQ-005",
        defaults={"nome": "Máquina de Solda MIG", "status": "parado", "setor": setor3}
    )
    print(f"  ✓ {eq5.tag} - {eq5.nome} {'(novo)' if created else '(existente)'}\n")

    # Criar Ordens de Serviço
    print("📋 Criando ordens de serviço...")
    os1, created = OrdemServico.objects.get_or_create(
        titulo="Revisão preventiva",
        equipamento=eq1,
        defaults={"status": "Aberta"}
    )
    print(f"  ✓ OS#{os1.id} - {os1.titulo} ({os1.status}) {'(novo)' if created else '(existente)'}")

    os2, created = OrdemServico.objects.get_or_create(
        titulo="Substituição de correia",
        equipamento=eq2,
        defaults={"status": "Em andamento"}
    )
    print(f"  ✓ OS#{os2.id} - {os2.titulo} ({os2.status}) {'(novo)' if created else '(existente)'}")

    os3, created = OrdemServico.objects.get_or_create(
        titulo="Limpeza geral",
        equipamento=eq3,
        defaults={"status": "Concluída", "data_conclusao": timezone.now()}
    )
    print(f"  ✓ OS#{os3.id} - {os3.titulo} ({os3.status}) {'(novo)' if created else '(existente)'}")

    os4, created = OrdemServico.objects.get_or_create(
        titulo="Calibração de sensores",
        equipamento=eq4,
        defaults={"status": "Aberta"}
    )
    print(f"  ✓ OS#{os4.id} - {os4.titulo} ({os4.status}) {'(novo)' if created else '(existente)'}")

    os5, created = OrdemServico.objects.get_or_create(
        titulo="Reparo de fiação elétrica",
        equipamento=eq5,
        defaults={"status": "Aberta"}
    )
    print(f"  ✓ OS#{os5.id} - {os5.titulo} ({os5.status}) {'(novo)' if created else '(existente)'}\n")

    # Exibir resumo
    print("\n" + "="*60)
    print("📊 RESUMO DOS DADOS")
    print("="*60)
    print(f"Empresas: {Empresa.objects.count()}")
    print(f"Setores: {Setor.objects.count()}")
    print(f"Equipamentos: {Equipamento.objects.count()}")
    print(f"Ordens de Serviço: {OrdemServico.objects.count()}\n")

    print("🟢 NÍVEL DE RISCO EQUIPAMENTOS:")
    for eq in Equipamento.objects.all():
        print(f"  {eq.tag}: {eq.nivel_risco.upper()}")

    print("\n✅ Dados iniciais carregados com sucesso!")
    print("="*60)

except Exception as e:
    print(f"\n❌ Erro ao carregar dados: {e}")
    import traceback
    traceback.print_exc()
