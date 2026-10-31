# devops-capstone-project
# Buckaroo's Bargains - Customer Accounts Microservice

![CI Build](https://github.com/mayuri3390/devops-capstone-project/actions/workflows/ci-build.yaml/badge.svg)

## Project Overview
This repository contains the cloud-native Customer Accounts microservice for Buckaroo's Bargains. The application is built using Python (Flask), PostgreSQL, and containerized with Docker. Continuous Integration is automated via GitHub Actions, and Continuous Delivery is managed using Tekton pipelines on OpenShift/Kubernetes.

## Features
- **RESTful APIs:** Full CRUD operations for customer account management.
- **Security:** Flask-Talisman security headers and Flask-CORS policy enforcement.
- **Testing:** Automated unit testing using `pytest` / `nosetests` with code coverage reports.
- **CI/CD:** Automated builds, linting via `flake8`, unit testing, and container deployment.

## Repository Structure
- `service/` - Microservice source code and routes
- `tests/` - Unit tests for models and routes
- `.github/workflows/` - Continuous Integration workflows
- `tekton/` - Continuous Delivery pipeline definitions
