# FastAPI CRUD

## Welcome to a simple but curated FastAPI CRUD example app

## Features

- 🔐 **OAuth2 + JWT Authentication** with role-based access control
- 🗃️ **Async SQLAlchemy** with PostgreSQL support
- 🔄 **Soft Delete** pattern with flexible filtering
- 📊 **Pagination** support for list endpoints
- ✅ **Pydantic v2** validation with custom validators
- 🐳 **Docker** deployment ready
- 🧪 **90%+ test coverage** with pytest
- ⚡ **Request timing** middleware

### Table of Contents

- [Features](#features)
- [Project structure](#project-structure)
- [Set up and run the app](#setup-and-run-app)
- [Run tests](#run-tests)
- [Docker Deployment](#docker-deployment)

## Project Structure

The app structure was designed to keep it simple, however organized.

- The expected configuration to run the app properly is expected to be
in the `core` folder, which also expects any security and middleware layers.
- The `models` folder contains all the model definitions the app uses. It includes
mixin classes for reusing logic.
- Within the `routers` folders live all the router modules per domain. This folder
has the dependency functions to be injected into the endpoint definitions to run.
- The `schemas` folder will handle the input and output data, including
their validations.
- All code-related business logic must be in the `services` folder. Not only the
logic with database operations, but also with custom validator services for
business rules, database integrity, and credentials.
- There's still space for helper functions, generic pagination, and custom
validations in the `utils` folder.

## Setup and run app

To run the FastAPI app, you need to install the uv package
manager and for getting all the dependencies run:

Create a new Python virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
uv sync
```

Also, it is important to have the required environment variables. You can
copy the `.env.example` file and customize it for your local
development:

```bash
cp .env.example .env
```

We need to run migrations first in order to run the app:

```bash
alembic upgrade head
```

> [!WARNING]
> Configure variables and run migrations before continuing

Now, you can run the app, which, as it is a typical FastAPI app, you can run with:

```bash
uv run uvicorn app.main:app --reload
```

## Run tests

Once you have achieved running the app, you can run the tests to ensure
everything is correct. Also serves as a guard for any new changes and
detects any code that could break the app:

```bash
uv run pytest
```

## Docker Deployment

Using Docker Compose
Start all services (PostgreSQL, API, Adminer):

```bash
docker compose up -d
```

View logs:

```bash
docker compose logs -f api
```

Stop services:

```bash
docker compose down
```

Build:

```bash
docker compose build
```
