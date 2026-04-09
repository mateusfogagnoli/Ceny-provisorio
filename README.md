# CENY
## 📦 Stack

| Componente | Tecnologia |
|-----------|-----------|
| Backend | Django 6.0, Django REST Framework 3.16 |
| Frontend | Vue.js 3, Vite, Vue Router, Axios |
| Database | SQLite |
| Python | 3.10+ |
| Node.js | 16+ |

## 🚀 Quick Start

### 1. Backend Setup

```bash
# Criar e ativar venv
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar e rodar
pip install -r requirements.txt
python manage.py migrate
python load_initial_data.py  # (opcional)
python manage.py runserver
```

Backend: `http://127.0.0.1:8000`

### 2. Frontend Setup

```bash
# Em outro terminal, ative o venv
cd school-management/ceny-vue
npm install
npm run dev
```

Frontend: `http://localhost:5173`

## 📋 Funcionalidades

- **CRUD completo**: Empresas, Setores, Equipamentos, Ordens de Serviço
- **Indicador de Risco**: Verde (0 OS) → Amarelo (1-2) → Vermelho (3+)
- **Validação de Fluxo**: Aberta → Em andamento → Concluída
- **Interface responsiva**: Abas navegáveis e mensagens em tempo real

## 🔌 API Principal

Base: `http://127.0.0.1:8000/api/maintenance/`

```
/empresas/           # CRUD de empresas
/setores/            # CRUD de setores
/equipamentos/       # CRUD de equipamentos + indicador risco
/ordens-servico/     # CRUD de ordens + gerenciamento status
```

## 📁 Estrutura

```
ceny/
├── app/                    # Config Django
├── maintenance/            # App principal (models, API)
├── school-management/
│   └── ceny-vue/          # Frontend Vue.js
├── db.sqlite3             # Banco
├── manage.py
├── requirements.txt
└── load_initial_data.py
```
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstale as dependências
pip install -r requirements.txt
```

### Erro: "Address already in use :8000"
```bash
# O servidor Django já está rodando
# Mate o processo ou use outra porta
python manage.py runserver 8001
```

### Erro: "npm: not found"
```bash
# Instale Node.js em: https://nodejs.org/
# Depois instale novamente:
npm install
```

### CORS Error no navegador
```
# Certifique-se que o backend está rodando
# Verifique se a URL em services/api.js está correta:
# http://127.0.0.1:8000/api/maintenance
```

---

## 📝 Sobre o db.sqlite3


### Como funciona sem db.sqlite3

1. Ao clonar o repositório, o `db.sqlite3` não virá
2. Execute `python manage.py migrate` para criar um novo banco vazio
3. (Opcional) Execute `python load_initial_data.py` para dados de teste

---
