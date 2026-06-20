# Task Tracker API — Production-like DevOps Platform

Pet-проєкт для портфоліо Junior DevOps інженера. Демонструє повний цикл розробки та експлуатації застосунку в хмарі.

## 🏗️ Архітектура

```
GitHub → CI/CD → GHCR → EC2
                          ├── Nginx (reverse proxy)
                          ├── FastAPI (Docker)
                          ├── PostgreSQL (Docker)
                          └── Grafana Alloy (моніторинг)
                                    ↓
                          Grafana Cloud (метрики + логи)
```

## 🛠️ Стек технологій

| Категорія | Технологія |
|---|---|
| Застосунок | FastAPI, PostgreSQL, SQLAlchemy 2.0, Pydantic v2 |
| Контейнеризація | Docker, Docker Compose |
| IaC | Terraform (VPC, EC2, S3, IAM) |
| Config Management | Ansible |
| CI/CD | GitHub Actions |
| Реєстр образів | GitHub Container Registry (GHCR) |
| Хмара | AWS (EC2 t3.micro, S3, SSM Parameter Store) |
| Reverse Proxy | Nginx |
| Моніторинг | Grafana Cloud (Prometheus + Loki) |
| Секрети | AWS SSM Parameter Store |

## 🚀 CI/CD Pipeline

```
git push → Lint (ruff) → Tests (pytest) → Build Docker → Push GHCR → Deploy (Ansible)
```

## 📁 Структура проєкту

```
├── app/                    # FastAPI застосунок
├── tests/                  # pytest тести
├── Dockerfile              # Multi-stage build, non-root user
├── docker-compose.yml      # App + PostgreSQL
├── terraform/              # IaC: VPC, EC2, S3, IAM
├── ansible/                # Provisioning + Deploy
│   └── roles/
│       ├── server_setup/   # UFW, fail2ban, timezone
│       ├── docker/         # Docker Engine + GHCR login
│       ├── nginx/          # Reverse proxy
│       └── app_deploy/     # Docker Compose deploy
└── .github/workflows/
    ├── ci.yml              # Lint → Test → Build → Push
    └── cd.yml              # Deploy to EC2
```

## 🔒 Безпека

- Секрети в AWS SSM Parameter Store (не в коді)
- Non-root user в Docker контейнері
- UFW firewall (тільки 22, 80, 443)
- fail2ban (захист SSH)
- SSH тільки з конкретного IP
- API доступний тільки через Nginx (127.0.0.1:8000)

## 📊 Моніторинг

- CPU, RAM, диск — Grafana Cloud (Prometheus)
- Логи контейнерів і Nginx — Grafana Cloud (Loki)
- Бекапи БД — щоночі о 2:00 UTC в S3

## 🏃 Запуск

### Передумови
- AWS акаунт
- Terraform >= 1.9
- Ansible >= 2.17
- Docker

### Кроки
```bash
# 1. Інфраструктура
cd terraform
./bootstrap.sh
terraform init && terraform apply

# 2. Provisioning сервера
cd ansible
ansible-playbook playbook.yml -i inventory.ini

# 3. Далі автоматично через CI/CD при git push
```

## 🌐 API Endpoints

| Method | Endpoint | Опис |
|---|---|---|
| GET | /health | Healthcheck |
| GET | /tasks | Список задач |
| POST | /tasks | Створити задачу |
| GET | /tasks/{id} | Отримати задачу |
| PUT | /tasks/{id} | Оновити задачу |
| DELETE | /tasks/{id} | Видалити задачу |

## 📝 Що навчився

- Terraform: IaC, remote state, модульність
- Ansible: roles, handlers, templates, idempotency
- GitHub Actions: CI/CD pipelines, secrets, environments
- Docker: multi-stage builds, health checks, networking
- AWS: EC2, VPC, S3, IAM, SSM Parameter Store
- Nginx: reverse proxy, security headers
- Grafana: метрики, логи, дашборди
