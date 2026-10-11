# 🍽️ TastyBites – Containerized Restaurant Web Application


A restaurant website (Flask + MySQL) packaged as a multi-container Docker stack. The focus of this project is the DevOps workflow around the application: containerization, orchestration with Docker Compose, reverse proxying, health checks, persistent storage, automated testing, CI and image vulnerability scanning.

---

## 📐 Architecture

```
Browser ──► :80  Nginx (reverse proxy)
                   │
                   ▼
              Flask + Gunicorn  (web, :5000)
                   │
                   ▼
              MySQL 8.0  (db)  ── named volume (db_data)

GitHub push ─► GitHub Actions: lint → test → build → Trivy scan → push image to GHCR
```

| Container | Image | Purpose |
|-----------|-------|---------|
| `nginx` | `nginx:1.27-alpine` | Reverse proxy, the only service published to the host (port 80) |
| `web` | built from `Dockerfile` | Flask app served by Gunicorn |
| `db` | `mysql:8.0` | MySQL database with a persistent volume |

---

## ✨ Features

**Application**
- User registration and login (bcrypt password hashing, CSRF-protected forms)
- Menu page with a client-side shopping cart
- Contact form with validation

**DevOps**
- Multi-stage Dockerfile with a non-root runtime user and a container `HEALTHCHECK`
- Docker Compose with health-based startup ordering (`depends_on: condition: service_healthy`)
- Database port not published to the host (default compose file)
- Persistent storage through a named Docker volume; schema created automatically from `init.sql`
- Configuration and credentials through environment variables (`.env`), with a dedicated non-root database user
- `/health` endpoint used by Docker health checks
- Automated tests with pytest and linting with flake8
- CI pipeline with GitHub Actions: lint, test, image build, Trivy vulnerability scan, push to GitHub Container Registry
- Makefile for common tasks (start, stop, logs, lint, test, backup, scan)

---

## 🧰 Tech Stack

Python · Flask · Flask-WTF · Gunicorn · MySQL · Nginx · Docker · Docker Compose · GitHub Actions · Trivy · pytest · flake8 · Make

---

## 📁 Project Structure

```
.
├── app.py
├── forms.py
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── Dockerfile
├── docker-compose.yml               # standard setup (Docker host / VPS / local machine)
├── docker-compose.codespaces.yml    # workaround for GitHub Codespaces (host networking)
├── init.sql
├── Makefile
├── .env.example
├── .dockerignore
├── .gitignore
├── nginx/
│   ├── default.conf
│   └── codespaces.conf
├── templates/                       # Jinja2 HTML templates
├── static/                          # CSS, JS, images
├── tests/
│   └── test_app.py
└── .github/workflows/
    └── docker.yml                   # CI pipeline
```

---

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose v2
- Git

### Run

```bash
# 1. Clone
git clone https://github.com/DurgaVarun/TastyBites-Containerized-Web-Application-Docker-.git
cd TastyBites-Containerized-Web-Application-Docker-

# 2. Configure environment
cp .env.example .env
# Edit .env and set your own values

# 3. Build and start the stack
docker compose up -d --build

# 4. Check status (db and web should become "healthy")
docker compose ps
```

Open **http://localhost**.

### Running on GitHub Codespaces

In my Codespace the default Docker bridge network did not allow container-to-container traffic, so I added a compose file that uses host networking:

```bash
docker compose -f docker-compose.codespaces.yml up -d --build
```

Then open port **80** from the **Ports** tab. On a normal Docker host or VPS, use `docker-compose.yml`.

### Environment variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Flask session and CSRF secret |
| `MYSQL_ROOT_PASSWORD` | MySQL root password (used by the DB container only) |
| `MYSQL_DATABASE` | Database name (default `tastybites`) |
| `MYSQL_USER` | Application database user |
| `MYSQL_PASSWORD` | Application database password |

> ⚠️ `.env` is listed in `.gitignore` and must never be committed.

---

## 🗄️ Database

MySQL 8.0 with one table, `users` (`id`, `username`, `email`, `password`, `created_at`). Passwords are stored as bcrypt hashes. The schema is created from `init.sql` the first time the database container starts with an empty volume.

```bash
docker compose exec db mysql -uroot -p
```

---

## 🛠️ Common Commands

```bash
make up        # build and start all containers
make down      # stop containers (data is kept)
make logs      # follow logs
make lint      # run flake8
make test      # run the pytest suite
make backup    # dump the database to backup.sql
make scan      # build the image and scan it with Trivy
```

On Codespaces, pass the compose command:

```bash
make up COMPOSE="docker compose -f docker-compose.codespaces.yml"
make backup COMPOSE="docker compose -f docker-compose.codespaces.yml"
```

Other useful commands:

```bash
docker compose logs -f web        # app logs
docker compose down -v            # stop and DELETE the database volume
docker compose exec web whoami    # prints "appuser" (non-root)
```

---

## 🔄 CI Pipeline

Every push and pull request to `main` triggers GitHub Actions (`.github/workflows/docker.yml`):

1. **Lint**: flake8
2. **Test**: pytest
3. **Build**: Docker image build
4. **Scan**: Trivy checks the image for HIGH and CRITICAL vulnerabilities
5. **Publish** (on `main` only): push the image to GitHub Container Registry, tagged with the commit SHA and `latest`

---

## 🔐 Security Practices

- Passwords hashed with bcrypt; CSRF protection on all forms
- Container runs as a non-root user
- No secrets in the codebase or image; configuration through environment variables and `.dockerignore`
- Database port not published to the host in the standard compose file
- Dedicated application database user (not root)
- Pinned image versions and automated image vulnerability scanning in CI

---

## 🐛 Troubleshooting

| Problem | Fix |
|---------|-----|
| `Table 'users' doesn't exist` | `init.sql` runs only on first DB start. Run `docker compose down -v`, then start again |
| `Access denied for user` | Passwords in `.env` changed after the volume was created. Reset the volume with `down -v` |
| Nginx returns 504 on Codespaces | Use `docker-compose.codespaces.yml` (see above) |
| 502 on the forwarded Codespaces URL | The containers are not running. Start the stack again |
| Mount error for `default.conf` | The file is missing, so Docker created a folder. Remove it and recreate the file |
| `TemplateNotFound` | HTML files must be inside `templates/` and match the names used in `app.py` |

---

## 🗺️ Roadmap

- [x] Dockerized Flask app (multi-stage build, non-root user, health check)
- [x] Docker Compose stack: Nginx + Gunicorn + MySQL
- [x] Persistent database volume and automatic schema creation
- [x] Environment-based configuration
- [x] Automated tests and linting
- [x] CI pipeline with Trivy scanning
- [x] Makefile for common tasks
- [ ] Separate frontend and backend Docker networks
- [ ] HTTPS and deployment to a server
- [ ] Automated deployment from GitHub Actions
- [ ] Monitoring with Prometheus and Grafana
- [ ] Orders table and persistent cart

---



**Durga Varun Minnekanti**
[GitHub](https://github.com/DurgaVarun) · [LinkedIn](https://www.linkedin.com/in/<your-profile>)
