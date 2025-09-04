## 📝 Project: Todo Flask App (CRUD with SQLite)
A clean, production-ready **Flask** Todo application showcasing **Create/Read/Update/Delete** with **SQLite** and server-rendered templates.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Localhost%205000-blue?logo=google-chrome)](http://localhost:5000)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-blue)

> **Why this app?** Great for lab practice: routing, forms, validation, database ops, and deploying a small Flask service.

---

## 📦 Tech Stack
- **Backend:** Python, Flask, Jinja2
- **DB:** SQLite (`todo.db` via `sqlite3` / `SQLAlchemy` optional)
- **Frontend:** HTML, CSS (in `templates/` and `static/`)
- **CI/CD:** GitHub Actions → Azure Web Apps (`.github/workflows/azure-webapps-python.yml`)

## 📂 Project Layout
```
KailashSatkuri-warangal/
│-- .github/workflows/azure-webapps-python.yml  # CI/CD to Azure Web Apps
│-- static/icon/                                # Static assets (icons)
│-- templates/                                  # Jinja2 HTML templates
│-- app.py                                      # Flask application
│-- todo.db                                     # SQLite database (local dev)
│-- .gitignore                                  # Ignored files
│-- README.md                                   # This file
```

---

## ⚙️ Setup (Local)
1) **Clone & enter repo**
```bash
git clone <your-fork-or-origin>
cd KailashSatkuri-warangal
```
2) **Virtual env & deps**
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # if missing, see below
```
3) **Environment variables** (create `.env` at repo root)
```
FLASK_ENV=development
SECRET_KEY=change-me
DATABASE_URL=sqlite:///todo.db
```
4) **Run app**
```bash
python app.py
# open http://127.0.0.1:5000/
```

> **No `requirements.txt`?** Generate one:
```bash
pip freeze > requirements.txt
```

---

## 🗃️ Database Model (Suggested)
A minimal `tasks` table (SQLite):
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `title` TEXT NOT NULL
- `completed` INTEGER DEFAULT 0
- `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP

**Initialize schema (SQLite CLI):**
```sql
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔌 Routes / Endpoints (Typical)
> Your exact routes may vary; align these with `app.py`.

| Method | Path            | Purpose           |
|-------:|-----------------|-------------------|
| GET    | `/`             | List tasks        |
| POST   | `/add`          | Create task       |
| POST   | `/update/<id>`  | Toggle/Update     |
| POST   | `/delete/<id>`  | Delete task       |

**cURL quick test:**
```bash
curl -X POST -d "title=Buy milk" http://127.0.0.1:5000/add
```

---

## 🧪 Quality: Testing & Linting
- **Tests:** `pytest`
- **Lint/Format:** `flake8`, `black`

```bash
pip install pytest flake8 black
pytest -q
flake8 .
black .
```

**Optional pre-commit hook** (create `.pre-commit-config.yaml`):
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.4.2
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    rev: 7.1.0
    hooks:
      - id: flake8
```
```bash
pip install pre-commit && pre-commit install
```

---

## 🧰 Docker (Optional)
**Dockerfile (example)**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_ENV=production
ENV PORT=8000
EXPOSE 8000
CMD ["python", "app.py"]
```
```bash
docker build -t todo-flask .
docker run -p 8000:8000 todo-flask
```

---

## 🚀 Deploy: Azure Web Apps (via GitHub Actions)
This repo already contains **`.github/workflows/azure-webapps-python.yml`**.

1. **Create Web App** in Azure (Linux, Python runtime).
2. In **GitHub → Settings → Secrets and variables → Actions** add:
   - `AZURE_WEBAPP_NAME` = your-app-name
   - `AZURE_PUBLISH_PROFILE` = content of Azure publish profile (XML)
3. **Push to main** → CI builds & deploys.
4. Configure **App Settings** in Azure:
   - `FLASK_ENV=production`
   - `SECRET_KEY=<secure-random>`
   - `DATABASE_URL=sqlite:///site.db` (or Azure storage if needed)

> For DB persistence on Azure, consider an external DB (Azure SQL / Postgres) instead of a local file.

---

## 🔀 Contributing via Forks (What you asked for)
We **do not store screenshots** in this repo and we accept changes **through forks + PRs**.

### A) Keep your fork in sync with upstream
```bash
git remote add upstream https://github.com/<owner>/KailashSatkuri-warangal.git
git fetch upstream
git checkout main
git merge upstream/main
# or: git rebase upstream/main
```

### B) Feature workflow
```bash
git checkout -b feat/<short-description>
# commit changes
git push origin feat/<short-description>
# open Pull Request from your fork → upstream
```

### C) Enforce "no screenshots" rule
Add these to **.gitignore**:
```
# block large media and screenshots
assets/
media/
screenshots/
*.png
*.jpg
*.jpeg
*.gif
*.bmp
```
**Optional:** Prevent image files from being committed (pre-commit hook):
```yaml
- repo: local
  hooks:
    - id: block-binary-images
      name: Block image additions
      entry: bash -c 'git diff --cached --name-only | grep -Ei "\.(png|jpe?g|gif|bmp)$" && echo "Images are not allowed" && exit 1 || exit 0'
      language: system
```
> This ensures forks cannot add screenshots; the hook fails before commit. For CI enforcement, add a job that greps PR changes and fails if images are added.

---

## 🔒 Security
- Never commit secrets. Use `.env` locally and **Actions Secrets** / Azure App Settings in prod.
- Rotate `SECRET_KEY` if leaked.

## 🧾 License
MIT © Kailash Satkuri

---

## 📚 Learning Outcomes (for students)
- RESTful thinking with Flask routes
- Server-side rendering with Jinja2
- SQLite schema design & CRUD
- CI/CD pipeline to Azure Web Apps
- Collaboration via fork → PR flow (and policy enforcement)


