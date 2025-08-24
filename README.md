# API de Cursos — FastAPI + MongoDB

Guia passo a passo para rodar o projeto localmente.

> **Stack**: FastAPI, Uvicorn, MongoDB (Motor), Pydantic, python-dotenv

---

## 1) Requisitos

* **Python 3.10+** (recomendado)
* **pip** (geralmente já vem com o Python)
* **Virtualenv** (opcional, mas recomendado)
* **MongoDB Community Server** instalado e rodando localmente

  * Porta padrão: `27017`
  * Cliente de shell (opcional): **mongosh**
* **Git** (para clonar o repositório)

> Se você ainda não tem o MongoDB instalado, instale a edição Community para o seu sistema operacional. Após instalar, garanta que o serviço esteja em execução (veja a seção **3) Subir o MongoDB**).

---

## 2) Estrutura esperada do projeto

```
project/
│── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── routers/
│   │   └── cursos.py
│── requirements.txt
│── .env
│── .gitignore
```

> O CRUD usa o campo **`codigo`** como identificador único dos cursos (evita depender do `_id` do MongoDB).

---

## 3) Subir o MongoDB

Certifique-se de que o serviço do MongoDB está rodando. Alguns comandos comuns:

* **Linux (systemd)**

  ```bash
  sudo systemctl start mongod
  sudo systemctl status mongod
  ```
* **macOS (Homebrew)**

  ```bash
  brew services start mongodb-community
  brew services list | grep mongodb
  ```
* **Windows**

  * Abra **Serviços** e inicie **MongoDB** (ou **MongoDB Server**),
  * ou use o **MongoDB Compass** para verificar a conexão.

---

## 4) Clonar o projeto

```bash
git clone <URL-do-seu-repo>
cd <pasta-do-repo>
```

> Substitua `<URL-do-seu-repo>` pelo endereço do seu GitHub.

---

## 5) Criar e ativar o ambiente virtual

* **Linux/macOS**

  ```bash
  python3 -m venv ambiente-virtual
  source ambiente-virtual/bin/activate
  ```
* **Windows (PowerShell)**

  ```powershell
  python3 -m venv ambiente-virtual   
  .\ambiente-virtual\Scripts\activate
  ```

> Para desativar depois: `deactivate`

---

## 6) Variáveis de ambiente

Crie um arquivo **`.env`** na raiz do projeto com o conteúdo abaixo (ajuste se necessário):

```env
MONGO_URI=mongodb://localhost:27017
MONGO_DB=meu_banco
```

---

## 7) Instalar dependências

Com o ambiente virtual **ativado**:

```bash
pip install -r requirements.txt
```

> Se você ainda não tem o `requirements.txt`, crie-o com:
>
> ```bash
> pip install fastapi uvicorn motor python-dotenv pydantic
> pip freeze > requirements.txt
> ```

---

## 8) (Opcional) Popular o banco com dados de exemplo

Com o **mongosh**:

```javascript
use meu_banco

db.cursos.insertMany([
  {
    codigo: "fastapi101",
    titulo: "FastAPI do Zero",
    descricao: "Aprenda FastAPI passo a passo",
    carga_horaria: 20
  },
  {
    codigo: "py-avancado",
    titulo: "Python Avançado",
    descricao: "Padrões, dicas e boas práticas",
    carga_horaria: 30
  }
])
```

> Ajuste o nome do DB (`meu_banco`) para o mesmo valor configurado no `.env`.

---

## 9) Rodar a API

Na raiz do projeto, com o venv ativado:

```bash
uvicorn app.main:app --reload
```

Saída esperada:

```
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

* **Docs interativas (Swagger)**: `http://127.0.0.1:8000/docs`
* **Redoc**: `http://127.0.0.1:8000/redoc`

---

## 10) Testar os endpoints (CRUD de cursos)

### Listar todos

```bash
curl -X GET http://127.0.0.1:8000/cursos/
```

### Criar novo curso

```bash
curl -X POST http://127.0.0.1:8000/cursos/ \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": "fastapi102",
    "titulo": "FastAPI na Prática",
    "descricao": "Construindo APIs reais",
    "carga_horaria": 24
  }'
```

### Buscar por código

```bash
curl -X GET http://127.0.0.1:8000/cursos/fastapi102
```

### Atualizar por código

```bash
curl -X PUT http://127.0.0.1:8000/cursos/fastapi102 \
  -H "Content-Type: application/json" \
  -d '{
    "descricao": "API completa com autenticação",
    "carga_horaria": 28
  }'
```

### Deletar por código

```bash
curl -X DELETE http://127.0.0.1:8000/cursos/fastapi102
```

> **Observação**: o campo `codigo` deve ser **único**. Se tentar criar um curso com um `codigo` já existente, a API retornará **400**.

---

## 11) Boas práticas

* **Não** versione credenciais: mantenha-as em `.env` (listado no `.gitignore`).
* Gere/atualize o `requirements.txt` sempre que adicionar libs: `pip freeze > requirements.txt`.
* Rodar a API a partir da **raiz** do projeto para evitar problemas de import.
* Configure um **índice único** opcional no Mongo para o campo `codigo`:

  ```javascript
  db.cursos.createIndex({ codigo: 1 }, { unique: true })
  ```

---

## 12) Erros comuns & soluções

* **Erro de conexão com o MongoDB**: verifique se o serviço está ativo e se `MONGO_URI` está correto.
* **`ModuleNotFoundError` / `uvicorn: command not found`**: confirme que o venv está ativo e as dependências instaladas.
* **CORS (em frontend)**: adicione o middleware de CORS no `app/main.py` se for consumir a API de um navegador.

---

## 13) .gitignore sugerido (resumo)

```gitignore
__pycache__/
*.py[cod]
venv/
env/
.venv/
ambiente-virtual/
.vscode/
.idea/
*.log
.DS_Store
Thumbs.db
.env
*.secret
```

---

## 14) Próximos passos

* Adicionar validação/normalização do `codigo` (ex.: slugify sem espaços)
* Implementar autenticação/autorização
* Testes automatizados (pytest) e pipeline CI
* Docker/Compose para subir API e MongoDB juntos
