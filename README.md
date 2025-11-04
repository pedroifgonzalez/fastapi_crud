# FastAPI CRUD

## Welcome to a simple but curated FastAPI CRUD example app

### Table of Contents

- Project structure
- Set up and run the app
- Run tests

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

```uv sync```

Also, it is important to have the required environment variables. You can
copy the `.env.example` file and customize it for your local
development:

```cp .env.example .env```

> [!WARNING]
> Configure variables before continuing

Now, you can run the app, which, as it is a typical FastAPI app, you can run with:

```uv run uvicorn app.main:app --reload```

## Run tests

Once you have achieved running the app, you can run the tests to ensure
everything is correct. Also serves as a guard for any new changes and
detects any code that could break the app:

```uv run pytest```
