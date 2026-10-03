# TastyBites-Containerized-Web-Application-Docker-
# 🍽️ TastyBites – Containerized Restaurant Web Application


A restaurant website (Flask + MySQL) packaged as a production-style, multi-container Docker stack. The focus of this project is the **DevOps workflow around the app**: containerization, orchestration, network isolation, health checks, CI, and image security scanning.

---

## 📐 Architecture

```
                 ┌────────────────────────── Docker host ──────────────────────────┐
                 │                                                                   │
  Browser ──► :80│  ┌─────────┐  frontend net  ┌──────────────────┐  backend net    │
                 │  │  Nginx  │ ─────────────► │  Flask/Gunicorn  │ ────────────►   │
                 │  │ (proxy) │                │   (web, :5000)   │      ┌────────┐ │
                 │  └─────────┘                └──────────────────┘      │ MySQL  │ │
                 │                                                       │  (db)  │ │
                 │                                    named volume ───►  └────────┘ │
                 └───────────────────────────────────────────────────────────────────┘

  GitHub push ─► GitHub Actions: lint → test → build → Trivy scan → push image
```

| Container | Image | Purpose |
|-----------|-------|---------|
| `nginx` | `nginx:1.27-alpine` | Reverse proxy, the only service exposed to the host |
| `web` | built from `Dockerfile` | Flask app served by Gunicorn |
| `db` | `mysql:8.0` | Database with persistent volume, on an internal-only network |

---

## ✨ Features

**Application**
- User registration and login (bcrypt password hashing, CSRF-protected forms)
- Menu page with a client-side shopping cart
- Contact form with validation

**DevOps**
- Multi-stage Dockerfile, non-root runtime user, container `HEALTHCHECK`
- Docker Compose orchestration with health-based startup ordering (`depends_on: service_healthy`)
- Network isolation: the database sits on an `internal` network with no published ports and no route to the internet
- Persistent storage using a named volume; schema auto-created from `init.sql`
- Configuration and credentials via environment variables (`.env`), with a least-privilege DB user
- CI pipeline with GitHub Actions: lint (flake8), tests (pytest), image build, Trivy vulnerability scan, push to registry
- Makefile for common operations (start, stop, logs, test, backup, scan)

---

## 🧰 Tech Stack

Python · Flask · Flask-WTF · Gunicorn · MySQL · Nginx · Docker · Docker Compose · GitHub Actions · Trivy · Make

---

## 📁 Project Structure

```
tastybites/
├── app.py
├── forms.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── init.sql
├── Makefile
├── .env.example
├── .dockerignore
├── .gitignore
├── nginx/
│   └── default.conf
├── templates/          # Jinja2 HTML templates
├── static/             # CSS, JS, images
├── tests/
│   └── test_app.py
└── .github/workflows/
    └── docker.yml      # CI pipeline
```

---

## 🚀 Getting Started

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and Docker Compose v2
- Git

### Run locally

```bash
# 1. Clone
git clone https://github.com/<your-username>/tastybites.git
cd tastybites

# 2. Configure environment
cp .env.example .env
# Edit .env and set strong values for all secrets

# 3. Build and start the stack
docker compose up -d --build

# 4. Check status
docker compose ps
```

Open **http://localhost** in your browser.

### Environment variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Flask session/CSRF secret key |
| `MYSQL_ROOT_PASSWORD` | MySQL root password (used by the DB container only) |
| `MYSQL_DATABASE` | Database name (default `tastybites`) |
| `MYSQL_USER` | Application DB user |
| `MYSQL_PASSWORD` | Application DB password |

> ⚠️ Never commit your `.env` file.

---

## 🛠️ Common Commands

```bash
make up        # build and start all containers
make down      # stop containers (data is kept)
make logs      # follow logs
make test      # run the test suite in a container
make backup    # dump the database to backup.sql
make scan      # scan the image with Trivy
```

Without Make:

```bash
docker compose logs -f web        # app logs
docker compose down -v            # stop and DELETE the database volume
docker exec -it <db-container> mysql -u root -p   # DB shell
```

---

## 🔄 CI Pipeline

Every push to `main` triggers GitHub Actions:

1. **Lint** – flake8
2. **Test** – pytest
3. **Build** – Docker image build with layer caching
4. **Scan** – Trivy checks the image for HIGH/CRITICAL vulnerabilities
5. **Publish** – push the versioned image to the container registry

---

## 🔐 Security Practices

- Passwords hashed with bcrypt; CSRF protection on all forms
- Container runs as a non-root user
- No secrets in the codebase or image; all configuration via environment variables
- Database not exposed to the host or the internet
- Least-privilege application DB user (not root)
- Pinned image versions and automated image vulnerability scanning

---

## 🐛 Troubleshooting

| Problem | Fix |
|---------|-----|
| `Table 'users' doesn't exist` | `init.sql` runs only on first DB start. Run `docker compose down -v`, then start again |
| `Access denied for user` | Passwords in `.env` changed after the volume was created. Reset the volume |
| Web container can't connect to DB | Ensure `MYSQL_HOST=db` and the DB container is healthy (`docker compose ps`) |
| Templates not found | HTML files must be inside `templates/` |

---

## 🗺️ Future Improvements

- Prometheus and Grafana monitoring containers
- HTTPS with Let's Encrypt via Caddy or Certbot
- Automated deployment to a VPS over SSH from GitHub Actions
- Docker secrets instead of environment variables
- Orders table and persistent cart

---


## 📄 License

This project is licensed under the MIT License.
